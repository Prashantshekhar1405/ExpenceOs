from rest_framework.routers import DefaultRouter
from .views import NotificationViewsets
router = DefaultRouter()

router.register("notifications" , NotificationViewsets , basename="notification")

urlpatterns = router.urls