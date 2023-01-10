import datetime
import logging

import feedparser

import db
from models.model_messages import MAILDROP_TYPES

LOGGER = logging.getLogger('applog')

MAX_LENGTH = 950  # TODO сделать единую константу в коде


def make_news():
    # TODO этот функционал будет заменён на подтягивание заголовков новостей из разных rss-лент, заданных в бд

    today_datetime = datetime.datetime.now()
    id_maildrop_type = MAILDROP_TYPES['news']
    last_sent_message = db.db_messages.get_last_sent_maildrop_by_type(id_maildrop_type)
    if last_sent_message:
        delta_dates = today_datetime - last_sent_message.date_create
        delta_hours = divmod(delta_dates.total_seconds(), 3600)[0]

    if not last_sent_message or (today_datetime.hour == 7 and today_datetime.minute == 0) or (today_datetime.hour >= 7 and delta_hours >= 3):
        feed = feedparser.parse('https://habr.com/ru/rss/news/?fl=ru')
        if feed:
            mes_news = ''
            separator = ' *** '
            for feed_entry in feed.entries:
                if len(mes_news) + len(feed_entry.title) + len(separator) < MAX_LENGTH:
                    mes_news += f'{feed_entry.title}{separator}'
                else:
                    break

            db.db_messages.create_message_maildrop(id_maildrop_type, mes_news)
