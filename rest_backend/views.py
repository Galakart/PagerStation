from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import DirectMessage, Pager, PrivateMessage
from .serializers import (DirectMessageSerializer,
                          MessageBySubscriberNumberSerializer)


class DirectMessageViewSet(viewsets.ModelViewSet):
    serializer_class = DirectMessageSerializer
    queryset = DirectMessage.objects.all()
    http_method_names = ['post', 'head', 'options']  # without 'get'


class MessageBySubscriberNumberViewSet(viewsets.ViewSet):
    serializer_class = MessageBySubscriberNumberSerializer

    def create(self, request):
        post_data = request.data
        subscriber_number = post_data['subscriber_number']
        message = post_data['message']

        try:
            id_pager = Pager.objects.get(
                subscriber_number=subscriber_number).id
        except Pager.DoesNotExist:
            return Response({'status': 'fail'}, status=status.HTTP_404_NOT_FOUND)

        PrivateMessage.objects.create(pager_id=id_pager, message=message)
        return Response({'status': 'ok'})
