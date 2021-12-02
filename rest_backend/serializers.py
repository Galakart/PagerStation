
from rest_framework import serializers

from .models import DirectMessage, PrivateMessage


class DirectMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectMessage
        fields = ('capcode', 'freq', 'fbit', 'message')


class MessageBySubscriberNumberSerializer(serializers.Serializer):
    subscriber_number = serializers.IntegerField(label='Абонентский номер')
    message = serializers.CharField(max_length=100, label='Сообщение')
