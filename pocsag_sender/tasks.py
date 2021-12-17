import os
import time
from contextlib import contextmanager

from django.core.cache import cache
from pagerstation.celery import app
from rest_backend.models import (DirectMessage, NewsChannel, NewsMessage,
                                 Pager, PrivateMessage, Transmitter)

from . import charset_encoder

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
            # for i in range(15):
            #     print(f'now to {i}')
            #     time.sleep(1)

            direct_messages = DirectMessage.objects.filter(is_sent=False)[:10]
            for direct_message in direct_messages:
                if os.path.exists('./pocsag'):
                    print('Sending direct POCSAG!')
                    message_text = charset_encoder.encode_message(
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

            private_messages = PrivateMessage.objects.filter(is_sent=False)[
                :10]
            for private_message in private_messages:
                if os.path.exists('./pocsag'):
                    print('Sending private POCSAG!')
                    id_pager = private_message.pager_id
                    capcode = Pager.objects.get(id=id_pager).capcode
                    capcode = f'{capcode:07d}'
                    fbit = Pager.objects.get(id=id_pager).fbit
                    id_transmitter = Pager.objects.get(
                        id=id_pager).transmitter_id
                    freq = Transmitter.objects.get(id=id_transmitter).freq
                    message_text = charset_encoder.encode_message(
                        private_message.message, 2)  # TODO передавать правильную кодировку
                    os.system(
                        f'echo "{capcode}:{message_text}" | sudo ./pocsag -f "{freq}" -b {fbit} -t 1')
                else:
                    print(
                        'Transmitter is not connected, so private message will be sent VIRTUALLY.')
                    time.sleep(10)
                PrivateMessage.objects.filter(
                    pk=private_message.pk).update(is_sent=True)

            news_messages = NewsMessage.objects.filter(is_sent=False)[:10]
            for news_message in news_messages:
                if os.path.exists('./pocsag'):
                    print('Sending news POCSAG!')
                    id_category = news_message.category
                    news_channels = NewsChannel.objects.filter(
                        category=id_category)
                    for news_channel in news_channels:
                        capcode = news_channel.capcode
                        capcode = f'{capcode:07d}'
                        fbit = news_channel.fbit
                        id_transmitter = news_channel.transmitter_id
                        freq = Transmitter.objects.get(id=id_transmitter).freq
                        message_text = charset_encoder.encode_message(
                            news_message.message, 2)  # TODO передавать правильную кодировку
                        os.system(
                            f'echo "{capcode}:{message_text}" | sudo ./pocsag -f "{freq}" -b {fbit} -t 1')
                else:
                    print(
                        'Transmitter is not connected, so news message will be sent VIRTUALLY.')
                    time.sleep(10)
                NewsMessage.objects.filter(
                    pk=news_message.pk).update(is_sent=True)
