from __future__ import absolute_import, unicode_literals
from pagerstation.celery import app
from django.conf import settings as conf_settings

from rest_backend.models import DirectMessage

IS_POCSAG_TRANSMITTER_CONNECTED = conf_settings.IS_POCSAG_TRANSMITTER_CONNECTED


@app.task
def hello_world():
    messages = DirectMessage.objects.filter(is_sent=False)
    for message in messages:
        print(message.capcode)
        DirectMessage.objects.filter(pk=message.pk).update(is_sent=True)
        if not IS_POCSAG_TRANSMITTER_CONNECTED:
            print('Sending pocsag!')
            continue
