import datetime
import logging

import db
from models.model_messages import MAILDROP_TYPES

from . import rss_feeder

LOGGER = logging.getLogger('applog')


def make_news():
    today_datetime = datetime.datetime.now()
    id_maildrop_type = MAILDROP_TYPES['news']
    last_sent_message = db.db_messages.get_last_sent_maildrop_by_type(id_maildrop_type)
    if last_sent_message:
        delta_dates = today_datetime - last_sent_message.date_create
        delta_hours = divmod(delta_dates.total_seconds(), 3600)[0]

    if not last_sent_message or (today_datetime.hour == 7 and today_datetime.minute == 0) or (today_datetime.hour >= 7 and delta_hours >= 3):
        rss_feed_item = db.db_messages.get_rss_feed_by_maildrop_type(id_maildrop_type)
        if rss_feed_item:
            maildrop_text = rss_feeder.get_rss_text(rss_feed_item)

        if maildrop_text:
            db.db_messages.create_message_maildrop(id_maildrop_type, maildrop_text)
