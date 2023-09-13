
import logging
import os
from logging.handlers import TimedRotatingFileHandler

import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from backend.jobs import fetcher_celebrations, fetcher_maildrop
# from backend.jobs import pocsag_messages
from backend.routers import \
    router_users  # router_direct, router_hardware, router_users

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
scheduler = BackgroundScheduler()
app.include_router(router_users.router)
# app.include_router(router_direct.router)
# app.include_router(router_hardware.router)


if not os.path.exists('logs'):
    os.makedirs('logs')
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
file_handler = TimedRotatingFileHandler(
    './logs/botlog.log',
    when='D',
    interval=1,
    backupCount=7,
)
file_handler.setFormatter(logging.Formatter('%(asctime)s  %(filename)s  %(funcName)s  %(lineno)d  %(name)s  %(levelname)s: %(message)s'))
LOGGER.addHandler(file_handler)


# @scheduler.scheduled_job('interval', id='do_job_pocsag_sender', seconds=5, misfire_grace_time=900)
# def job_pocsag_sender():
#     pocsag_messages.send_messages()


# @scheduler.scheduled_job('interval', id='do_job_maildrop_fetcher', seconds=60, misfire_grace_time=900)
# def job_maildrop_fetcher():
#     fetcher_maildrop.make_data()


# @scheduler.scheduled_job('cron', id='do_job_celebrations_fetcher', hour=0, minute=0)
# def job_celebrations_fetcher():
#     fetcher_celebrations.make_data()


# scheduler.start()


if __name__ == "__main__":  # режим отладки, запуск через "python -m backend"
    uvicorn.run("backend.__main__:app", host="0.0.0.0", port=8099, reload=True)
