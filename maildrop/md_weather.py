import datetime
import logging
import time

import config
import db
from models.model_messages import MAILDROP_TYPES
from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config

LOGGER = logging.getLogger('applog')


def make_forecast():
    today_datetime = datetime.datetime.now()

    id_maildrop_type = MAILDROP_TYPES['weather']
    last_sent_message = db.db_messages.get_last_sent_maildrop_by_type(id_maildrop_type)
    if last_sent_message:
        delta_dates = today_datetime - last_sent_message.date_create
        delta_hours = divmod(delta_dates.total_seconds(), 3600)[0]

    if not last_sent_message or (today_datetime.hour in (7, 14, 21) and today_datetime.minute == 0) or delta_hours > 24:
        try:
            config_dict = get_default_config()
            config_dict['language'] = 'ru'
            config_dict['connection'] = {
                "timeout_secs": 30,
                "max_retries": 3,
            }
            owm = OWM(config.OWM_TOKEN, config_dict)
            mgr = owm.weather_manager()
            w = mgr.weather_at_place(config.OWM_CITY).weather

            temp = round(w.temperature('celsius')['temp'])
            if temp > 0:
                temp = f'+{temp}'
            status = w.detailed_status
            hum = w.humidity
            sunrise = time.strftime("%H:%M", time.localtime(w.sunrise_time(timeformat='unix')))
            sunset = time.strftime("%H:%M", time.localtime(w.sunset_time(timeformat='unix')))

            owm_forecast_tomorrow = mgr.forecast_at_place(config.OWM_CITY, '3h').get_weather_at(timestamps.tomorrow())
            temp_tomorrow = round(owm_forecast_tomorrow.temperature('celsius')['temp'])
            if temp_tomorrow > 0:
                temp_tomorrow = f'+{temp_tomorrow}'
            status_tomorrow = owm_forecast_tomorrow.detailed_status

            mes_weather = f'Погода. Сейчас: {temp}, {status}, влажность {hum}%, восход: {sunrise}, закат: {sunset} *** Завтра: {temp_tomorrow}, {status_tomorrow}'
        except Exception as ex:
            LOGGER.error('Ошибка получения данных о погоде\n %s', ex, exc_info=True)
            return

        db.db_messages.create_message_maildrop(id_maildrop_type, mes_weather)
