import datetime
import logging
from http import HTTPStatus

import feedparser
import requests

from backend.constants import MESSAGE_MAX_LENGTH
from backend.db import db_messages
from backend.db.connection import SessionLocal
from backend.models.enums import MaildropTypeEnum
from backend.models.model_channels import MaildropRssFeed
from backend.models.model_messages import (Message, MessageSchema,
                                           MessageTypeEnum)

LOGGER = logging.getLogger()
TIMEOUT = 10


url_currency = 'https://api.coingate.com/v2'
url_currency_additional_ping = '/ping'
url_currency_additional_usdrub = '/rates/merchant/USD/RUB'
url_currency_additional_eurrub = '/rates/merchant/EUR/RUB'
url_currency_additional_btcrub = '/rates/merchant/BTC/RUB'
currency_preferred_hours = [7]  # обновление раз в день в 7:00


def update_maildrop():
    """Обновление новостного контента и оформление его в виде maildrop сообщений"""
    # Для фиксированных новостных тем (погода, курс валют, новости) вначале производится
    # проверка, не привязана ли к этой теме RSS-лента. Если привязана, то контент будет браться из неё,
    # если нет - будет скачиваться из публичных работающих на данный момент REST-сервисов в методах ниже

    # контент обновляется в часы, указанные в переменных "..._preferred_hours" (в 00 минут),
    # или принудительно в любое время если прошлое обновление было больше суток назад

    # update_forecast()
    update_currency()
    # update_news()
    # update_rss()


def update_currency():
    id_maildrop_type = MaildropTypeEnum.CURRENCY

    with SessionLocal() as session:
        last_sent_message = db_messages.get_last_sent_maildrop_by_type(session, id_maildrop_type)
        if not _is_need_update(last_sent_message, currency_preferred_hours):
            return

        maildrop_text = None
        rss_feed_item = db_messages.get_rss_feed_by_maildrop_type(session, id_maildrop_type)
        if rss_feed_item:
            maildrop_text = _get_rss_text(rss_feed_item)
        else:
            try:
                response_ping = requests.get(f'{url_currency}{url_currency_additional_ping}', timeout=TIMEOUT)
                if response_ping.status_code == HTTPStatus.OK:
                    cur_usd = requests.get(f'{url_currency}{url_currency_additional_usdrub}', timeout=TIMEOUT).text
                    cur_eur = requests.get(f'{url_currency}{url_currency_additional_eurrub}', timeout=TIMEOUT).text
                    cur_btc = requests.get(f'{url_currency}{url_currency_additional_btcrub}', timeout=TIMEOUT).text

                    maildrop_text = f'Курс валют. Доллар: {cur_usd} руб. Евро: {cur_eur} руб. Биткоин: {cur_btc} руб.'
                # TODO логирование если response не удался

            except Exception as ex:
                LOGGER.error('Ошибка получения курсов валют\n %s', ex, exc_info=True)
                return

        if maildrop_text:
            message_schema_item = MessageSchema(
                uid=None,
                id_message_type=MessageTypeEnum.MAILDROP,
                id_pager=None,
                id_group_type=None,
                id_maildrop_type=id_maildrop_type,
                message=maildrop_text,
                sent=None,
                datetime_send_after=None,
                datetime_create=None,
            )

            db_messages.create_message(session, message_schema_item)


def _is_need_update(message: Message, preferred_hours_lst: list[int]) -> bool:
    if not message:
        return True

    today_datetime = datetime.datetime.now()
    delta_hours = divmod((today_datetime - message.datetime_create).total_seconds(), 3600)[0]
    if (today_datetime.hour in preferred_hours_lst and today_datetime.minute == 0) or delta_hours > 24:
        return True

    return False


def _get_rss_text(rss_feed_item: MaildropRssFeed):
    feed = feedparser.parse(rss_feed_item.feed_link)
    if feed:
        rss_text = ''
        separator = ' *** '

        # Наполняем сообщение загруженными заголовками RSS-статей (с самой свежей), пока не упрёмся
        # в ограничение MESSAGE_MAX_LENGTH. Если уже самая первый заголовок превышает это ограничение -
        # возьмём только его, обрезав всё что за пределами
        is_first_item = True
        for feed_entry in feed.entries:
            if len(rss_text) + len(feed_entry.title) + len(separator) < MESSAGE_MAX_LENGTH:
                rss_text += f'{feed_entry.title}{separator}'
                is_first_item = False
            else:
                if is_first_item:
                    rss_text = feed_entry.title[:MESSAGE_MAX_LENGTH]
                break

        return rss_text
