from rest_framework.routers import DefaultRouter

from .views import DirectMessageViewSet, MessageBySubscriberNumberViewSet

router = DefaultRouter()
router.register(r'directmessages', DirectMessageViewSet)
router.register(r'privatemessages',
                MessageBySubscriberNumberViewSet,
                basename='privatemessages'
                )

urlpatterns = router.urls
