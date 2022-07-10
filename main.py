"""Main module"""
#!venv/bin/python

import datetime
import logging
import logging.handlers as loghandlers
import os
import time

import requests
# from flask_restful import Api, Resource
from flask import Flask, request
from flask_apscheduler import APScheduler
from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config

import config
import db
from charset_encoder import CharsetEncoder
from models.mdl_messages import MAILDROP_TYPES
from models.mdl_pagers import Baudrate, Codepage, Transmitter

app = Flask(__name__)
# api = Api(app)

charset_encoder = CharsetEncoder()

scheduler = APScheduler()
scheduler.api_enabled = config.IS_TEST
scheduler.init_app(app)


if not os.path.exists('logs'):
    os.makedirs('logs')
LOGGER = logging.getLogger('applog')
LOGGER.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s  %(filename)s  %(funcName)s  %(lineno)d  %(name)s  %(levelname)s: %(message)s')
log_handler = loghandlers.RotatingFileHandler(
    './logs/botlog.log',
    maxBytes=1000000,
    encoding='utf-8',
    backupCount=10
)
log_handler.setLevel(logging.INFO)
log_handler.setFormatter(formatter)
LOGGER.addHandler(log_handler)


# class ToAdmin(Resource):
#     def get(self):
#         return "<h1>ololo</h1>"


# api.add_resource(ToAdmin, '/toadmin/')

@app.route('/toadmin/', methods=['GET', 'POST'])
def form_example():
    if request.method == 'POST':
        mes_text = request.form.get('mes_text')[:950]
        if not mes_text:
            return """
                <CENTER>
                    <p><b>Введите сообщение!!!</b></p>
                    <a href="./">назад</a>
                </CENTER>
                """

        admins_tuple = db.dbops_users.get_admins()
        if admins_tuple:
            for admin_item in admins_tuple:
                pagers = db.dbops_users.get_user_pagers(admin_item.id)
                for pager_item in pagers:
                    db.dbops_messages.create_message_private(pager_item.id, mes_text)
        else:
            return """
                <CENTER>
                    <p><b>Админов в сервисе не зарегистрировано</b></p>
                    <a href="./">назад</a>
                </CENTER>
                """

        return """
                <CENTER>
                    <p><b>Сообщение отправлено</b></p>
                    <a href="./">назад</a>
                </CENTER>
                """

    return """
            <CENTER>
                <H2>Отправь сообщение админу на пейджер</H2>
                <form method="POST">
                    <p><b>Текст сообщения:</b></p>
                    <textarea name="mes_text" rows=10 cols=80 maxlength=950 required></textarea>
                    <br /><br />
                    <input type="submit" value="Отправить">
                </form>
            </CENTER>
            """


@scheduler.task('interval', id='do_job_pocsag_sender', seconds=5, misfire_grace_time=900)
def job_pocsag_sender():

    unsent_messages_private_tuple = db.dbops_messages.get_unsent_messages_private()
    if unsent_messages_private_tuple:
        for unsent_message_private_item in unsent_messages_private_tuple:
            pager_item = db.dbops_pagers.get_pager(unsent_message_private_item.id_pager)
            transmitter_item = db.dbops_classifiers.find_classifier_object(Transmitter, pager_item.id_transmitter)
            baudrate_item = db.dbops_classifiers.find_classifier_object(Baudrate, transmitter_item.id_baudrate)
            codepage_item = db.dbops_classifiers.find_classifier_object(Codepage, pager_item.id_codepage)
            message_to_air(pager_item.capcode, pager_item.id_fbit, transmitter_item.freq,
                           baudrate_item.name, codepage_item.id, unsent_message_private_item.message)
            db.dbops_messages.mark_message_private_sent(unsent_message_private_item.id)

    unsent_messages_maildrop_tuple = db.dbops_messages.get_unsent_messages_maildrop()
    if unsent_messages_maildrop_tuple:
        for unsent_message_maildrop_item in unsent_messages_maildrop_tuple:
            maildrop_channels_tuple = db.dbops_messages.get_maildrop_channels_by_type(
                unsent_message_maildrop_item.id_maildrop_type)
            for maildrop_channel_item in maildrop_channels_tuple:
                transmitter_item = db.dbops_classifiers.find_classifier_object(
                    Transmitter, maildrop_channel_item.id_transmitter)
                baudrate_item = db.dbops_classifiers.find_classifier_object(Baudrate, transmitter_item.id_baudrate)
                codepage_item = db.dbops_classifiers.find_classifier_object(Codepage, maildrop_channel_item.id_codepage)
                message_to_air(maildrop_channel_item.capcode, maildrop_channel_item.id_fbit,
                               transmitter_item.freq, baudrate_item.name, codepage_item.id, unsent_message_maildrop_item.message)
                db.dbops_messages.mark_message_maildrop_sent(unsent_message_maildrop_item.id)


@scheduler.task('interval', id='do_job_maildrop_picker', seconds=60, misfire_grace_time=900)
def job_maildrop_picker():
    today_datetime = datetime.datetime.now()

    # Погода
    id_maildrop_type = MAILDROP_TYPES['weather']
    last_sent_message = db.dbops_messages.get_last_sent_maildrop_by_type(id_maildrop_type)
    if last_sent_message:
        delta_dates = today_datetime - last_sent_message.date_create
        delta_hours = divmod(delta_dates.total_seconds(), 3600)[0]

    if not last_sent_message or (today_datetime.hour in (7, 14, 21) and today_datetime.minute == 0) or delta_hours > 24:
        try:
            config_dict = get_default_config()
            config_dict['language'] = 'ru'
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
            LOGGER.error(ex)
            mes_weather = 'Ошибка получения данных о погоде'

        db.dbops_messages.create_message_maildrop(id_maildrop_type, mes_weather)

    # Курс валют
    id_maildrop_type = MAILDROP_TYPES['currency']
    last_sent_message = db.dbops_messages.get_last_sent_maildrop_by_type(id_maildrop_type)
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
            LOGGER.error(ex)
            currency_mes = 'Ошибка получения курсов валют'

        db.dbops_messages.create_message_maildrop(id_maildrop_type, currency_mes)


scheduler.start()


def message_to_air(capcode: int, fbit: int, freq: int, baudrate: int, id_codepage: int, message: str) -> bool:
    """Отправляет сообщение в эфир

    Args:
        capcode (int): капкод
        fbit (int): id источника
        freq (int): частота в Гц
        baudrate (int): id скорости
        id_codepage (int): id кодировки текста
        message (str): сообщение

    Returns:
        bool: успех
    """
    capcode = f'{capcode:07d}'
    message_text = charset_encoder.encode_message(message, id_codepage)
    if not os.path.exists('./pocsag'):
        return False
    os.system(f'echo "{capcode}:{message_text}" | sudo ./pocsag -f "{freq}" -b {fbit} -r {baudrate} -t 1')
    return True


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8095, debug=config.IS_TEST)
