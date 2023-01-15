"""Main module"""
#!venv/bin/python
import datetime
import logging
import logging.handlers as loghandlers
import os

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Form, Path, Request
from fastapi.responses import FileResponse, HTMLResponse

import db
from maildrop import fetcher
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
def to_admin_form_action(request: Request, mes_text=Form()):
    client_ip = request.client.host
    if not mes_text:
        return """
            <CENTER>
                <p><b>Введите сообщение!!!</b></p>
                <a href="./to_admin">назад</a>
            </CENTER>
            """

    stricts_ipaddress_item = db.db_messages.get_stricts_ipaddress(client_ip)
    if stricts_ipaddress_item and stricts_ipaddress_item.last_send > datetime.datetime.now() - datetime.timedelta(minutes=1):
        return """
            <CENTER>
                <p><b>Установлено ограничение на 1 сообщение в минуту</b></p>
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

    db.db_messages.create_or_update_stricts_ipaddress(client_ip)
    return """
            <CENTER>
                <p><b>Сообщение отправлено</b></p>
                <a href="./to_admin">назад</a>
            </CENTER>
            """


@scheduler.scheduled_job('interval', id='do_job_pocsag_sender', seconds=5, misfire_grace_time=900)
def job_pocsag_sender():
    sender.send_messages()


@scheduler.scheduled_job('interval', id='do_job_maildrop_fetcher', seconds=60, misfire_grace_time=900)
def job_maildrop_fetcher():
    fetcher.pull_data()


scheduler.start()

# to run manually, exec:
# uvicorn main:app --reload --host 0.0.0.0 --port 8092
