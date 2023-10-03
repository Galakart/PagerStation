"""Backend main module"""
import logging
import os
from logging.handlers import TimedRotatingFileHandler

from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.jobs import job_maildrop, job_messages
from backend.routers import (router_channels, router_hardware, router_messages,
                             router_users, router_utils)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.include_router(router_hardware.router)
app.include_router(router_channels.router)
app.include_router(router_users.router)
app.include_router(router_messages.router)
app.include_router(router_utils.router)

scheduler = BackgroundScheduler(
    jobstores={
        'default': SQLAlchemyJobStore(url='sqlite:///./apscheduler.db')
    }
)

if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
file_handler = TimedRotatingFileHandler(
    './logs/applog.log',
    when='D',
    interval=1,
    backupCount=7,
)
file_handler.setFormatter(logging.Formatter('%(asctime)s  %(filename)s  %(funcName)s  \
                                            %(lineno)d  %(name)s  %(levelname)s: %(message)s'))
LOGGER.addHandler(file_handler)
logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)


@scheduler.scheduled_job('interval', id='do_job_send_messages', seconds=5, misfire_grace_time=900)
def job_send_messages():
    """Таймер для слежения за новыми сообщениями"""
    job_messages.send_messages()


@scheduler.scheduled_job('interval', id='do_job_update_maildrop', seconds=60, misfire_grace_time=900)
def job_update_maildrop_currency():
    """Таймер для обновления новостного (maildrop) контента"""
    job_maildrop.update_maildrop()


@scheduler.scheduled_job('cron', id='do_job_check_celebrations', hour=0, minute=0)
def job_check_celebrations():
    """Таймер проверки, наступило ли время праздников"""
    job_messages.check_celebrations()


scheduler.start()


# для запуска в режиме отладки (в консоли)
# uvicorn backend.__main__:app --host 0.0.0.0 --port 8099 --reload
