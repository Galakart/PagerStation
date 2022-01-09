import datetime

import requests
from django.utils import timezone
from rest_backend.models import NewsMessage

NEWS_CATEGORY = 4


def make_currency():
    today_date = datetime.datetime.now()
    max_last_create_time = timezone.now()-timezone.timedelta(hours=24)
    actual_mes_count = NewsMessage.objects.filter(
        category=NEWS_CATEGORY, date_create__gt=max_last_create_time).count()

    if (today_date.hour == 7 and today_date.minute == 0) or actual_mes_count == 0:
        try:
            response_ping = requests.get('https://api.coingate.com/v2/ping')
            if int(response_ping.status_code) == 200:
                cur_usd = requests.get(
                    'https://api.coingate.com/v2/rates/merchant/USD/RUB').text
                cur_eur = requests.get(
                    'https://api.coingate.com/v2/rates/merchant/EUR/RUB').text
                cur_btc = requests.get(
                    'https://api.coingate.com/v2/rates/merchant/BTC/RUB').text

                currency_mes = f'Курс валют. Доллар: {cur_usd} руб. *** Евро: {cur_eur} руб. *** Биткоин: {cur_btc} руб.'
            else:
                currency_mes = 'Нет данных о курсах валют'

        except Exception as ex:
            currency_mes = 'Ошибка получения курсов валют'
        NewsMessage(category=NEWS_CATEGORY, message=currency_mes).save()
