import datetime
import logging
import random

import db
from models.model_users import User

LOGGER = logging.getLogger('applog')


def make_data():
    make_birthdays()


def make_birthdays():
    users_tuple = db.db_users.get_users_with_birthday()
    user_item: User
    for user_item in users_tuple:
        if user_item.pagers:
            id_pager = user_item.pagers[0].id
            mes = 'Поздравляем с днём рождения!!!'

            today_date = datetime.date.today()
            datetime_send_after = datetime.datetime(
                year=today_date.year,
                month=today_date.month,
                day=today_date.day,
                hour=random.randint(9, 14),
                minute=random.randint(0, 59),
                second=0,
            )

            db.db_messages.create_message_private(id_pager, mes, datetime_send_after)
