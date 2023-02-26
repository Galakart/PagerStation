"""Main module"""
#!venv/bin/python
import logging
import logging.handlers as loghandlers
import os

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from maildrop import fetcher_celebrations, fetcher_maildrop
from pocsag_sender import sender
from routers import router_direct, router_hardware, router_users

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
scheduler = BackgroundScheduler()
app.include_router(router_direct.router)
app.include_router(router_hardware.router)
app.include_router(router_users.router)

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


@scheduler.scheduled_job('interval', id='do_job_pocsag_sender', seconds=5, misfire_grace_time=900)
def job_pocsag_sender():
    sender.send_messages()


@scheduler.scheduled_job('interval', id='do_job_maildrop_fetcher', seconds=60, misfire_grace_time=900)
def job_maildrop_fetcher():
    fetcher_maildrop.make_data()


@scheduler.scheduled_job('cron', id='do_job_celebrations_fetcher', hour=0, minute=0)
def job_celebrations_fetcher():
    fetcher_celebrations.make_data()


scheduler.start()

# to run manually, exec:
# uvicorn main:app --reload --host 0.0.0.0 --port 8092
