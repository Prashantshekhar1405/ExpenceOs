from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("user" , views.UserViewSet)
router.register("department" , views.DepartmentViewSet)

urlpatterns = router.urls