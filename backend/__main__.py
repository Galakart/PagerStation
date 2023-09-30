
import logging
import os
from logging.handlers import TimedRotatingFileHandler

import uvicorn
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
file_handler.setFormatter(logging.Formatter('%(asctime)s  %(filename)s  %(funcName)s  %(lineno)d  %(name)s  %(levelname)s: %(message)s'))
LOGGER.addHandler(file_handler)
logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)


@app.on_event('startup')
def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(job_messages.send_messages, 'interval', id='do_job_messages', seconds=5, misfire_grace_time=900)
    scheduler.add_job(job_maildrop.update_maildrop, 'interval', id='do_job_maildrop', seconds=60, misfire_grace_time=900)
    scheduler.add_job(job_messages.check_celebrations, 'cron', id='do_job_check_celebrations', hour=0, minute=0)

    scheduler.start()
    app.state.scheduler = scheduler


@app.on_event('shutdown')
def stop_scheduler():
    app.state.scheduler.shutdown(wait=False)


if __name__ == "__main__":  # режим отладки, запуск через "python -m backend"
    uvicorn.run("backend.__main__:app", host="0.0.0.0", port=8099, reload=True)
