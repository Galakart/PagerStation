import datetime
import time
from contextlib import contextmanager

from django.conf import settings as conf_settings
from django.core.cache import cache
from pagerstation.celery import app
from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
from rest_backend.models import NewsMessage

LOCK_EXPIRE = 60 * 10

TOKEN_OWM = conf_settings.TOKEN_OWM
WEATHER_CITY = conf_settings.WEATHER_CITY


@contextmanager
def memcache_lock(lock_id, oid):
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    status = cache.add(lock_id, oid, LOCK_EXPIRE)
    try:
        yield status
    finally:
        if time.monotonic() < timeout_at and status:
            cache.delete(lock_id)


@app.task(bind=True)
def pick_data(self):
    with memcache_lock(self.name, self.app.oid) as acquired:
        if acquired:
            today_date = datetime.datetime.now()
            if today_date.hour in (7, 14, 21):
                config_dict = get_default_config()
                config_dict['language'] = 'ru'
                owm = OWM(TOKEN_OWM, config_dict)
                mgr = owm.weather_manager()

                w = mgr.weather_at_place(WEATHER_CITY).weather

                temp = round(w.temperature('celsius')['temp'])
                status = w.detailed_status
                hum = w.humidity
                sunrise = time.strftime("%H:%M", time.localtime(
                    w.sunrise_time(timeformat='unix')))
                sunset = time.strftime("%H:%M", time.localtime(
                    w.sunset_time(timeformat='unix')))

                three_h_forecaster = mgr.forecast_at_place(WEATHER_CITY, '3h')
                weather = three_h_forecaster.get_weather_at(
                    timestamps.tomorrow())
                tomorrow_temp = round(weather.temperature('celsius')['temp'])
                tomorrow_status = weather.detailed_status

                weather_mes = f'Погода. Сейчас: {temp}, {status}, влажность {hum}%, восход: {sunrise}, закат: {sunset} *** Завтра: {tomorrow_temp}, {tomorrow_status}'

                NewsMessage(category=3, message=weather_mes).save()
