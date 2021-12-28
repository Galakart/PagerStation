import os

from rest_backend.models import (DirectMessage, NewsChannel, NewsMessage,
                                 Pager, PrivateMessage, Transmitter)

from .charset_encoder import CharsetEncoder

BATCH_LIMIT = 10

charset_encoder = CharsetEncoder()

#TODO проверка на существование объектов
def transmit_messages():
    direct_messages = DirectMessage.objects.filter(is_sent=False)[:BATCH_LIMIT]
    for direct_message in direct_messages:
        message_to_air(direct_message.capcode, direct_message.fbit,
                       direct_message.codepage, direct_message.message, direct_message.freq)
        DirectMessage.objects.filter(
            pk=direct_message.pk).update(is_sent=True)

    private_messages = PrivateMessage.objects.filter(is_sent=False)[:BATCH_LIMIT]
    for private_message in private_messages:
        id_pager = private_message.pager_id
        capcode = Pager.objects.get(id=id_pager).capcode
        fbit = Pager.objects.get(id=id_pager).fbit
        codepage = Pager.objects.get(id=id_pager).codepage
        freq = Transmitter.objects.get(
            id=Pager.objects.get(id=id_pager).transmitter_id).freq
        message_to_air(capcode, fbit, codepage,
                       private_message.message, freq)
        PrivateMessage.objects.filter(
            pk=private_message.pk).update(is_sent=True)

    news_messages = NewsMessage.objects.filter(is_sent=False)[:BATCH_LIMIT]
    for news_message in news_messages:
        id_category = news_message.category
        # может быть несколько каналов с одной категорией (для разных трансмиттеров или капкодов например)
        news_channels = NewsChannel.objects.filter(category=id_category)
        for news_channel in news_channels:
            capcode = news_channel.capcode
            fbit = news_channel.fbit
            codepage = news_channel.codepage
            freq = Transmitter.objects.get(id=news_channel.transmitter_id).freq
            message_to_air(capcode, fbit, codepage,
                           news_message.message, freq)
        NewsMessage.objects.filter(pk=news_message.pk).update(is_sent=True)


def message_to_air(capcode, fbit, codepage, message, freq):
    capcode = f'{capcode:07d}'
    message_text = charset_encoder.encode_message(message, codepage)
    if os.path.exists('./pocsag'):
        print('Sending new POCSAG!')
        os.system(
            f'echo "{capcode}:{message_text}" | sudo ./pocsag -f "{freq}" -b {fbit} -t 1')
    else:
        print('Transmitter is not connected, so message will be sent VIRTUALLY.')
