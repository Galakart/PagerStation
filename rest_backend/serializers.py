from rest_framework import serializers

from .models import MESSAGE_MAX_LENGTH, DirectMessage


class DirectMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessage
        fields = ('capcode', 'freq', 'fbit', 'message')


class MessageBySubscriberNumberSerializer(serializers.Serializer):
    subscriber_number = serializers.IntegerField(
        label='Абонентский номер',
    )
    message = serializers.CharField(
        label='Сообщение',
        max_length=MESSAGE_MAX_LENGTH,
    )
