from rest_framework.routers import DefaultRouter

from .views import DirectMessageViewSet

router = DefaultRouter()
router.register(r'directmessages', DirectMessageViewSet)

urlpatterns = router.urls