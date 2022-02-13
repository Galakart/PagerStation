import datetime

import requests
from django.utils import timezone
from rest_backend.models import MESSAGE_MAX_LENGTH, NewsMessage

NEWS_CATEGORY = 2


def make_news():
    today_date = datetime.datetime.now()
    max_last_create_time = timezone.now()-timezone.timedelta(hours=12)
    actual_mes_count = NewsMessage.objects.filter(
        category=NEWS_CATEGORY, date_create__gt=max_last_create_time).count()

    if (today_date.hour in (7, 19) and today_date.minute == 0) or actual_mes_count == 0:
        try:
            news_mes = 'Новости'
            news_all = requests.get(
                'https://meduza.io/api/v3/search?chrono=news&page=0&per_page=5&locale=ru').json()
            for item in news_all['documents']:
                if item[:5] != 'news/':
                    continue
                cur_news = (news_all['documents'][item]['title']).replace(
                    '«', '\"').replace('»', '\"').replace('„', '\"').replace('“', '\"').replace('\u00A0', ' ')
                if len(news_mes) + len(cur_news) + 5 <= MESSAGE_MAX_LENGTH:
                    news_mes = f'{news_mes} *** {cur_news}'

            NewsMessage(category=NEWS_CATEGORY, message=news_mes).save()
        except Exception as ex:
            pass
