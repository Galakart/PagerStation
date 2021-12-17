import os
import time
from contextlib import contextmanager

from django.conf import settings as conf_settings
from django.core.cache import cache
from pagerstation.celery import app
from pyowm import OWM
from pyowm.utils.config import get_default_config
from rest_backend.models import NewsMessage


LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes

TOKEN_OWM = conf_settings.TOKEN_OWM


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

            config_dict = get_default_config()
            config_dict['language'] = 'ru'
            owm = OWM(TOKEN_OWM, config_dict)
            mgr = owm.weather_manager()

            w = mgr.weather_at_place('Novokuznetsk').weather

            temp = round(w.temperature('celsius')['temp'])
            status = w.detailed_status
            hum = w.humidity
            sunrise = time.strftime("%H:%M", time.gmtime(
                w.sunrise_time(timeformat='unix')))
            sunset = time.strftime("%H:%M", time.gmtime(
                w.sunset_time(timeformat='unix')))

            weather_mes = f'Погода *** Сейчас: {temp}, {status}, влажность {hum}%, восход: {sunrise}, закат: {sunset}'

            # three_h_forecast = mgr.forecast_at_place('Novokuznetsk', '3h').forecast
            # print(len(three_h_forecast))
            # for weather in three_h_forecast:
            #     print(weather.reference_time)
            #     print(weather.temperature('celsius'))

            NewsMessage(category=3, message=weather_mes).save()
