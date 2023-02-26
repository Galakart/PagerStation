import datetime
import logging
import time

from pyowm import OWM
from pyowm.utils.config import get_default_config

import config
import db
from models.model_messages import MaildropTypeEnum

from . import rss_feeder

LOGGER = logging.getLogger('applog')

HOUR_MORNING = 7
HOUR_DAY = 14
HOUR_EVENING = 21


def make_forecast():
    today_datetime = datetime.datetime.now()

    id_maildrop_type = MaildropTypeEnum.WEATHER.value
    last_sent_message = db.db_messages.get_last_sent_maildrop_by_type(id_maildrop_type)
    if last_sent_message:
        delta_dates = today_datetime - last_sent_message.date_create
        delta_hours = divmod(delta_dates.total_seconds(), 3600)[0]

    if not last_sent_message or (today_datetime.hour in (HOUR_MORNING, HOUR_DAY, HOUR_EVENING) and today_datetime.minute == 0) or delta_hours > 24:
        rss_feed_item = db.db_messages.get_rss_feed_by_maildrop_type(id_maildrop_type)
        if rss_feed_item:
            maildrop_text = rss_feeder.get_rss_text(rss_feed_item)
        else:
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
                owm = OWM(config.OWM_TOKEN, config_dict)
                mgr = owm.weather_manager()
                one_call = mgr.one_call(lat=config.OWM_LATITUDE, lon=config.OWM_LONGITUDE)

                temp = round(one_call.current.temperature('celsius')['temp'])
                if temp > 0:
                    temp = f'+{temp}'
                status = one_call.current.detailed_status
                hum = one_call.current.humidity
                pressure_dict = one_call.current.barometric_pressure()
                pressure = round(pressure_dict['press'] * 0.75) if pressure_dict else "???"
                sunrise = time.strftime("%H:%M", time.localtime(one_call.current.sunrise_time(timeformat='unix')))
                sunset = time.strftime("%H:%M", time.localtime(one_call.current.sunset_time(timeformat='unix')))

                maildrop_text = 'Погода. '
                maildrop_text += f'Сейчас: {temp}, {status}, влажность {hum}%, давл. {pressure}мм.рт.ст., '
                maildrop_text += f'восход: {sunrise}, закат: {sunset} *** '

                if today_datetime.hour < HOUR_DAY:
                    delta_day = HOUR_DAY - today_datetime.hour
                    temp_day = round(one_call.forecast_hourly[delta_day].temperature('celsius')['temp'])
                    if temp_day > 0:
                        temp_day = f'+{temp_day}'
                    status_day = one_call.forecast_hourly[delta_day].detailed_status
                    maildrop_text += f'Днём: {temp_day}, {status_day} *** '
                elif today_datetime.hour >= HOUR_DAY and today_datetime.hour < HOUR_EVENING:
                    delta_eve = HOUR_EVENING - today_datetime.hour
                    temp_eve = round(one_call.forecast_hourly[delta_eve].temperature('celsius')['temp'])
                    if temp_eve > 0:
                        temp_eve = f'+{temp_eve}'
                    status_eve = one_call.forecast_hourly[delta_eve].detailed_status
                    maildrop_text += f'Вечером: {temp_eve}, {status_eve} *** '
                else:
                    temp_night = round(one_call.forecast_daily[0].temperature('celsius')['night'])
                    if temp_night > 0:
                        temp_night = f'+{temp_night}'
                    maildrop_text += f'Ночью: {temp_night} *** '

                status_tomorrow = one_call.forecast_daily[1].detailed_status
                temp_tomorrow_morn = round(one_call.forecast_daily[1].temperature('celsius')['morn'])
                if temp_tomorrow_morn > 0:
                    temp_tomorrow_morn = f'+{temp_tomorrow_morn}'
                temp_tomorrow_day = round(one_call.forecast_daily[1].temperature('celsius')['day'])
                if temp_tomorrow_day > 0:
                    temp_tomorrow_day = f'+{temp_tomorrow_day}'
                maildrop_text += f'Завтра: {status_tomorrow}, утром {temp_tomorrow_morn}, днём {temp_tomorrow_day}'

            except Exception as ex:
                LOGGER.error('Ошибка получения данных о погоде\n %s', ex, exc_info=True)
                return

        if maildrop_text:
            db.db_messages.create_message_maildrop(id_maildrop_type, maildrop_text)
