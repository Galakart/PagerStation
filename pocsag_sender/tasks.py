import os
import time
from contextlib import contextmanager

from django.conf import settings as conf_settings
from django.core.cache import cache
from pagerstation.celery import app
from rest_backend.models import DirectMessage, PrivateMessage, Pager, Transmitter

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
            for direct_message in direct_messages:
                if IS_POCSAG_TRANSMITTER_CONNECTED and os.path.exists('./pocsag'):
                    print('Sending direct POCSAG!')
                    message_text = encode_message(
                        direct_message.message, 2)
                    capcode = f'{direct_message.capcode:07d}'
                    os.system(
                        f'echo "{capcode}:{message_text}" | sudo ./pocsag -f "{direct_message.freq}" -b {direct_message.fbit} -t 1')
                else:
                    print(
                        'Transmitter is not connected, so direct message will be sent VIRTUALLY')
                    time.sleep(10)
                DirectMessage.objects.filter(
                    pk=direct_message.pk).update(is_sent=True)

            private_messages = PrivateMessage.objects.filter(is_sent=False)
            for private_message in private_messages:
                if IS_POCSAG_TRANSMITTER_CONNECTED and os.path.exists('./pocsag'):
                    print('Sending private POCSAG!')
                    id_pager = private_message.pager_id
                    capcode = Pager.objects.get(id=id_pager).capcode
                    capcode = f'{capcode:07d}'
                    fbit = Pager.objects.get(id=id_pager).fbit
                    id_transmitter = Pager.objects.get(
                        id=id_pager).transmitter_id
                    freq = Transmitter.objects.get(id=id_transmitter).freq
                    message_text = encode_message(
                        private_message.message, 2)  # TODO передавать правильную кодировку
                    os.system(
                        f'echo "{capcode}:{message_text}" | sudo ./pocsag -f "{freq}" -b {fbit} -t 1')
                else:
                    print(
                        'Transmitter is not connected, so private message will be sent VIRTUALLY.')
                    time.sleep(10)
                PrivateMessage.objects.filter(
                    pk=private_message.pk).update(is_sent=True)
