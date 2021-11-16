from __future__ import absolute_import, unicode_literals

import time
from contextlib import contextmanager

from django.conf import settings as conf_settings
from django.core.cache import cache
from pagerstation.celery import app
from rest_backend.models import DirectMessage

IS_POCSAG_TRANSMITTER_CONNECTED = conf_settings.IS_POCSAG_TRANSMITTER_CONNECTED


LOCK_EXPIRE = 60 * 10  # Lock expires in 10 minutes


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
def hello_world(self):
    with memcache_lock(self.name, self.app.oid) as acquired:
        if acquired:
            for i in range(30):
                print(f'now to {i}')
                time.sleep(1)

    # messages = DirectMessage.objects.filter(is_sent=False)
    # for message in messages:
    #     print(message.capcode)
    #     DirectMessage.objects.filter(pk=message.pk).update(is_sent=True)
    #     if not IS_POCSAG_TRANSMITTER_CONNECTED:
    #         print('Sending pocsag!')
    #         continue
