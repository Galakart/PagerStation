from rest_framework import viewsets


from .models import DirectMessage
from .serializers import DirectMessageSerializer


class DirectMessageViewSet(viewsets.ModelViewSet):
    serializer_class = DirectMessageSerializer
    queryset = DirectMessage.objects.all()
    http_method_names = ['post', 'head', 'options'] # without 'get'