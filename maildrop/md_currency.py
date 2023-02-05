import datetime
import logging

import requests

import db
from models.model_messages import MaildropTypes

from . import rss_feeder

LOGGER = logging.getLogger('applog')


def make_currency():
    today_datetime = datetime.datetime.now()

    id_maildrop_type = MaildropTypes.CURRENCY.value
    last_sent_message = db.db_messages.get_last_sent_maildrop_by_type(id_maildrop_type)
    if last_sent_message:
        delta_dates = today_datetime - last_sent_message.date_create
        delta_hours = divmod(delta_dates.total_seconds(), 3600)[0]

    if not last_sent_message or (today_datetime.hour == 7 and today_datetime.minute == 0) or delta_hours > 24:
        rss_feed_item = db.db_messages.get_rss_feed_by_maildrop_type(id_maildrop_type)
        if rss_feed_item:
            maildrop_text = rss_feeder.get_rss_text(rss_feed_item)
        else:
            try:
                response_ping = requests.get('https://api.coingate.com/v2/ping')
                if int(response_ping.status_code) == 200:
                    cur_usd = requests.get('https://api.coingate.com/v2/rates/merchant/USD/RUB').text
                    cur_eur = requests.get('https://api.coingate.com/v2/rates/merchant/EUR/RUB').text
                    cur_btc = requests.get('https://api.coingate.com/v2/rates/merchant/BTC/RUB').text

                    maildrop_text = f'Курс валют. Доллар: {cur_usd} руб. Евро: {cur_eur} руб. Биткоин: {cur_btc} руб.'
                else:
                    maildrop_text = 'Нет данных о курсах валют'

            except Exception as ex:
                LOGGER.error('Ошибка получения курсов валют\n %s', ex, exc_info=True)
                return

        if maildrop_text:
            db.db_messages.create_message_maildrop(id_maildrop_type, maildrop_text)
