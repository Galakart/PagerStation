import time
from contextlib import contextmanager

from django.core.cache import cache
from pagerstation.celery import app

from . import sender

LOCK_EXPIRE = 60 * 10


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
def transmit_messages(self):
    with memcache_lock(self.name, self.app.oid) as acquired:
        if acquired:
            sender.transmit_messages()
