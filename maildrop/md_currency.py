import datetime
import logging

import db
import requests
from models.model_messages import MAILDROP_TYPES

LOGGER = logging.getLogger('applog')


def make_currency():
    today_datetime = datetime.datetime.now()

    id_maildrop_type = MAILDROP_TYPES['currency']
    last_sent_message = db.db_messages.get_last_sent_maildrop_by_type(id_maildrop_type)
    if last_sent_message:
        delta_dates = today_datetime - last_sent_message.date_create
        delta_hours = divmod(delta_dates.total_seconds(), 3600)[0]

    if not last_sent_message or (today_datetime.hour == 7 and today_datetime.minute == 0) or delta_hours > 24:
        try:
            response_ping = requests.get('https://api.coingate.com/v2/ping')
            if int(response_ping.status_code) == 200:
                cur_usd = requests.get('https://api.coingate.com/v2/rates/merchant/USD/RUB').text
                cur_eur = requests.get('https://api.coingate.com/v2/rates/merchant/EUR/RUB').text
                cur_btc = requests.get('https://api.coingate.com/v2/rates/merchant/BTC/RUB').text

                currency_mes = f'Курс валют. Доллар: {cur_usd} руб. Евро: {cur_eur} руб. Биткоин: {cur_btc} руб.'
            else:
                currency_mes = 'Нет данных о курсах валют'

        except Exception as ex:
            LOGGER.error('Ошибка получения курсов валют\n %s', ex, exc_info=True)
            return

        db.db_messages.create_message_maildrop(id_maildrop_type, currency_mes)
