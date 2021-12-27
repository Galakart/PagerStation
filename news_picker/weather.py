import datetime
import time

from django.conf import settings as conf_settings
from django.utils import timezone
from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
from rest_backend.models import NewsMessage

TOKEN_OWM = conf_settings.TOKEN_OWM
WEATHER_CITY = conf_settings.WEATHER_CITY
NEWS_CATEGORY = 3

max_last_create_time = timezone.now()-timezone.timedelta(hours=7)
config_dict = get_default_config()
config_dict['language'] = 'ru'


def make_forecast():
    today_date = datetime.datetime.now()
    actual_mes_count = NewsMessage.objects.filter(
        category=NEWS_CATEGORY, date_create__gt=max_last_create_time).count()

    if (today_date.hour in (7, 14, 21) and today_date.minute == 0) or actual_mes_count == 0: #TODO поправить, лишняя отправка посреди ночи из-за истечения максимального периода
        try:
            owm = OWM(TOKEN_OWM, config_dict)
            mgr = owm.weather_manager()

            owm_weather = mgr.weather_at_place(WEATHER_CITY).weather
            temp = round(owm_weather.temperature('celsius')['temp'])
            status = owm_weather.detailed_status
            hum = owm_weather.humidity
            sunrise = time.strftime("%H:%M", time.localtime(
                owm_weather.sunrise_time(timeformat='unix')))
            sunset = time.strftime("%H:%M", time.localtime(
                owm_weather.sunset_time(timeformat='unix')))

            owm_forecast_tomorrow = mgr.forecast_at_place(
                WEATHER_CITY, '3h').get_weather_at(timestamps.tomorrow())
            temp_tomorrow = round(
                owm_forecast_tomorrow.temperature('celsius')['temp'])
            status_tomorrow = owm_forecast_tomorrow.detailed_status

            weather_mes = f'Погода. Сейчас: {temp}, {status}, влажность {hum}%, восход: {sunrise}, закат: {sunset} *** Завтра: {temp_tomorrow}, {status_tomorrow}'
            NewsMessage(category=NEWS_CATEGORY, message=weather_mes).save()
        except Exception as ex:
            pass
