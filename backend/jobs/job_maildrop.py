"""Периодические действия - новостной контент"""
import datetime
import logging
import time
from http import HTTPStatus

import feedparser
import requests
from pyowm import OWM
from pyowm.utils.config import get_default_config

from backend.config_reader import config as appconf
from backend.constants import MESSAGE_MAX_LENGTH
from backend.db import db_channels, db_messages
from backend.db.connection import SessionLocal
from backend.models.enums import MaildropTypeEnum
from backend.models.model_messages import (Message, MessageSchema,
                                           MessageTypeEnum)

LOGGER = logging.getLogger()
TIMEOUT = 10


HOUR_MORNING = 7
HOUR_DAY = 14
HOUR_EVENING = 21
weather_preferred_hours = [HOUR_MORNING, HOUR_DAY, HOUR_EVENING]  # обновление в 7:00, 14:00, 21:00

URL_CURRENCY = 'https://api.coingate.com/v2'
URL_CURRENCY_ADDITIONAL_PING = '/ping'
URL_CURRENCY_ADDITIONAL_USDRUB = '/rates/merchant/USD/RUB'
URL_CURRENCY_ADDITIONAL_EURRUB = '/rates/merchant/EUR/RUB'
URL_CURRENCY_ADDITIONAL_BTCRUB = '/rates/merchant/BTC/RUB'
currency_preferred_hours = [7]  # обновление раз в день в 7:00

rss_preferred_hours = [7]  # обновление раз в день в 7:00


def update_maildrop():
    """Обновление новостного контента и оформление его в виде maildrop сообщений"""
    # Для фиксированных новостных тем (погода, курс валют) вначале производится
    # проверка, привязана ли к этой теме RSS-лента.
    # Если нет - будет скачиваться из публичных работающих на данный момент REST-сервисов
    # в методах ниже

    # контент обновляется в часы, указанные в переменных "..._preferred_hours" (в 00 минут),
    # или принудительно в любое время если прошлое обновление было больше суток назад

    update_forecast()
    update_currency()
    update_rss()


def update_forecast():
    """Обновление прогноза погоды"""
    if not appconf.owm_token:
        return

    id_maildrop_type = MaildropTypeEnum.WEATHER
    today_datetime = datetime.datetime.now()

    with SessionLocal() as session:
        last_sent_message = db_messages.get_last_sent_maildrop_by_type(session, id_maildrop_type)
        if not _is_need_update(last_sent_message, weather_preferred_hours):
            return

        message_text = None
        rss_feed_item = db_channels.get_rss_feed_by_maildrop_type(session, id_maildrop_type)
        if rss_feed_item:
            return

        try:
            config_dict = get_default_config()
            config_dict['language'] = 'ru'
            config_dict['connection'] = {
                "use_ssl": True,
                "verify_ssl_certs": True,
                "use_proxy": False,
                "timeout_secs": 30,
                "max_retries": 3,
            }
            owm = OWM(appconf.owm_token.get_secret_value(), config_dict)
            mgr = owm.weather_manager()
            one_call = mgr.one_call(
                lat=float(appconf.owm_latitude),
                lon=float(appconf.owm_longitude)
            )
            assert isinstance(one_call.forecast_hourly, list)
            assert isinstance(one_call.forecast_daily, list)
        except Exception as ex:
            LOGGER.error('Ошибка получения данных о погоде\n %s', ex, exc_info=True)
            return

        temp = round(one_call.current.temperature('celsius')['temp'])
        if temp > 0:
            temp = f'+{temp}'
        status = one_call.current.detailed_status
        hum = one_call.current.humidity
        pressure_dict = one_call.current.barometric_pressure()
        pressure = round(pressure_dict['press'] * 0.75) if pressure_dict else "???"

        owm_sunrise = str(one_call.current.sunrise_time(timeformat='unix'))
        sunrise = time.strftime(
            "%H:%M",
            time.localtime(float(owm_sunrise))
        ) if owm_sunrise else '???'
        owm_sunset = str(one_call.current.sunset_time(timeformat='unix'))
        sunset = time.strftime(
            "%H:%M",
            time.localtime(float(owm_sunset))
        ) if owm_sunset else '???'

        message_text = 'Погода. '
        message_text += f'Сейчас: {temp}, {status}, влажность {hum}%, давл. {pressure}мм.рт.ст., '
        message_text += f'восход: {sunrise}, закат: {sunset} *** '

        if today_datetime.hour < HOUR_DAY:
            delta_day = HOUR_DAY - today_datetime.hour
            temp_day = round(one_call.forecast_hourly[delta_day].temperature('celsius')['temp'])
            if temp_day > 0:
                temp_day = f'+{temp_day}'
            status_day = one_call.forecast_hourly[delta_day].detailed_status
            message_text += f'Днём: {temp_day}, {status_day} *** '
        elif today_datetime.hour >= HOUR_DAY and today_datetime.hour < HOUR_EVENING:
            delta_eve = HOUR_EVENING - today_datetime.hour
            temp_eve = round(one_call.forecast_hourly[delta_eve].temperature('celsius')['temp'])
            if temp_eve > 0:
                temp_eve = f'+{temp_eve}'
            status_eve = one_call.forecast_hourly[delta_eve].detailed_status
            message_text += f'Вечером: {temp_eve}, {status_eve} *** '
        else:
            temp_night = round(one_call.forecast_daily[0].temperature('celsius')['night'])
            if temp_night > 0:
                temp_night = f'+{temp_night}'
            message_text += f'Ночью: {temp_night} *** '

        status_tomorrow = one_call.forecast_daily[1].detailed_status
        temp_tomorrow_morn = round(one_call.forecast_daily[1].temperature('celsius')['morn'])
        if temp_tomorrow_morn > 0:
            temp_tomorrow_morn = f'+{temp_tomorrow_morn}'
        temp_tomorrow_day = round(one_call.forecast_daily[1].temperature('celsius')['day'])
        if temp_tomorrow_day > 0:
            temp_tomorrow_day = f'+{temp_tomorrow_day}'
        message_text += (
            f'Завтра: {status_tomorrow}, утром {temp_tomorrow_morn}, днём {temp_tomorrow_day}'
        )

        _create_maildrop_message(session, id_maildrop_type, message_text)


def update_currency():
    """Обновление курсов валют"""
    id_maildrop_type = MaildropTypeEnum.CURRENCY

    with SessionLocal() as session:
        last_sent_message = db_messages.get_last_sent_maildrop_by_type(session, id_maildrop_type)
        if not _is_need_update(last_sent_message, currency_preferred_hours):
            return

        message_text = None
        rss_feed_item = db_channels.get_rss_feed_by_maildrop_type(session, id_maildrop_type)
        if rss_feed_item:
            return

        try:
            response_ping = requests.get(
                f'{URL_CURRENCY}{URL_CURRENCY_ADDITIONAL_PING}',
                timeout=TIMEOUT
            )
            if response_ping.status_code != HTTPStatus.OK:
                raise Exception

            cur_usd = requests.get(
                f'{URL_CURRENCY}{URL_CURRENCY_ADDITIONAL_USDRUB}',
                timeout=TIMEOUT
            ).text
            cur_eur = requests.get(
                f'{URL_CURRENCY}{URL_CURRENCY_ADDITIONAL_EURRUB}',
                timeout=TIMEOUT
            ).text
            cur_btc = requests.get(
                f'{URL_CURRENCY}{URL_CURRENCY_ADDITIONAL_BTCRUB}',
                timeout=TIMEOUT
            ).text

            message_text = (
                'Курс валют. '
                f'Доллар: {cur_usd} руб. '
                f'Евро: {cur_eur} руб. '
                f'Биткоин: {cur_btc} руб. '
            )

        except Exception as ex:
            LOGGER.error('Ошибка получения курсов валют\n %s', ex, exc_info=True)
            return

        _create_maildrop_message(session, id_maildrop_type, message_text)


def update_rss():
    """Обновление RSS-лент"""
    with SessionLocal() as session:
        rss_feeds = db_channels.get_rss_feeds(session)
        for feed_item in rss_feeds:
            last_sent_message = db_messages.get_last_sent_maildrop_by_type(
                session,
                feed_item.id_maildrop_type
            )
            if not _is_need_update(last_sent_message, rss_preferred_hours):
                continue

            message_text = None
            feed = feedparser.parse(feed_item.feed_link)
            if feed:
                message_text = ''
                separator = ' *** '

                # Наполняем сообщение загруженными заголовками RSS-статей (с самой свежей),
                # пока не упрёмся в ограничение MESSAGE_MAX_LENGTH.
                # Если уже самая первый заголовок превышает это ограничение -
                # возьмём только его, обрезав всё что за пределами
                is_first_item = True
                for feed_entry in feed.entries:
                    if len(message_text) + len(feed_entry.title) \
                            + len(separator) < MESSAGE_MAX_LENGTH:
                        message_text += f'{feed_entry.title}{separator}'
                        is_first_item = False
                    else:
                        if is_first_item:
                            message_text = feed_entry.title[:MESSAGE_MAX_LENGTH]
                        break

            if not message_text:
                LOGGER.error('Ошибка получения rss')
                continue

            _create_maildrop_message(session, feed_item.id_maildrop_type, message_text)


def _is_need_update(message: Message, preferred_hours_lst: list[int]) -> bool:
    if not message:
        return True

    today_datetime = datetime.datetime.now()
    delta_hours = divmod((today_datetime - message.datetime_create).total_seconds(), 3600)[0]
    if (today_datetime.hour in preferred_hours_lst and today_datetime.minute == 0) \
            or delta_hours > 24:
        return True

    return False


def _create_maildrop_message(session, id_maildrop_type, message_text):
    if message_text:
        message_schema_item = MessageSchema(
            uid=None,
            id_message_type=MessageTypeEnum.MAILDROP,
            id_pager=None,
            id_group_type=None,
            id_maildrop_type=id_maildrop_type,
            message=message_text,
            sent=None,
            datetime_send_after=None,
            datetime_create=None,
        )

        db_messages.create_message(session, message_schema_item)
