"""Main module"""
#!venv/bin/python

import datetime
import logging
import logging.handlers as loghandlers
import os
import time

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Form, Path
from fastapi.responses import FileResponse, HTMLResponse
from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config

import config
import db
from models.model_messages import MAILDROP_TYPES
from pocsag_sender import sender

app = FastAPI()
scheduler = BackgroundScheduler()


if not os.path.exists('logs'):
    os.makedirs('logs')
LOGGER = logging.getLogger('applog')
LOGGER.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s  %(filename)s  %(funcName)s  %(lineno)d  %(name)s  %(levelname)s: %(message)s')
log_handler = loghandlers.RotatingFileHandler(
    './logs/applog.log',
    maxBytes=1000000,
    encoding='utf-8',
    backupCount=10
)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(formatter)
LOGGER.addHandler(log_handler)


@app.get("/capcode_to_frame/{capcode}")
def capcode_to_frame(capcode: int = Path(ge=1, le=9999999)):
    return {"frame_number": capcode % 8}


@app.get("/to_admin", response_class=FileResponse)
def msg_for_admin_form():
    return "templates/to_admin.html"


@app.post("/to_admin_form_action", response_class=HTMLResponse)
def to_admin_form_action(mes_text=Form()):
    if not mes_text:
        return """
            <CENTER>
                <p><b>Введите сообщение!!!</b></p>
                <a href="./to_admin">назад</a>
            </CENTER>
            """

    admins_tuple = db.db_users.get_admins()
    if admins_tuple:
        for admin_item in admins_tuple:
            pagers = db.db_users.get_user_pagers(admin_item.id)
            for pager_item in pagers:
                db.db_messages.create_message_private(pager_item.id, mes_text)
    else:
        return """
            <CENTER>
                <p><b>Админов в сервисе не зарегистрировано</b></p>
                <a href="./to_admin">назад</a>
            </CENTER>
            """

    return """
            <CENTER>
                <p><b>Сообщение отправлено</b></p>
                <a href="./to_admin">назад</a>
            </CENTER>
            """


@scheduler.scheduled_job('interval', id='do_job_pocsag_sender', seconds=5, misfire_grace_time=900)
def job_pocsag_sender():
    sender.send_messages()


@scheduler.scheduled_job('interval', id='do_job_maildrop_picker', seconds=60, misfire_grace_time=900)
def job_maildrop_picker():
    today_datetime = datetime.datetime.now()

    # Погода
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

    # Курс валют
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


scheduler.start()


# to run manually, exec:
# uvicorn main:app --reload --host 0.0.0.0 --port 8092
