from __future__ import absolute_import, unicode_literals

import os
import time
from contextlib import contextmanager

from django.conf import settings as conf_settings
from django.core.cache import cache
from pagerstation.celery import app
from rest_backend.models import DirectMessage

from .pocsag_encoder import encode_message

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
def periodic_send(self):
    with memcache_lock(self.name, self.app.oid) as acquired:
        if acquired:
            # for i in range(30):
            #     print(f'now to {i}')
            #     time.sleep(1)
            direct_messages = DirectMessage.objects.filter(is_sent=False)
            if not direct_messages:
                print('no messages')
                return
            for direct_message in direct_messages:
                if IS_POCSAG_TRANSMITTER_CONNECTED and os.path.exists('./pocsag'):
                    print('Sending POCSAG!')
                    message_text = encode_message(
                        direct_message.message, 2)
                    capcode = f'{direct_message.capcode:07d}'
                    os.system(
                        f'echo "{capcode}:{message_text}" | sudo ./pocsag -f "{direct_message.freq}" -b {direct_message.fbit} -t 1')
                else:
                    print(
                        'Transmitter is not connected, so message will be sent VIRTUALLY')
                    time.sleep(10)
                DirectMessage.objects.filter(
                    pk=direct_message.pk).update(is_sent=True)
