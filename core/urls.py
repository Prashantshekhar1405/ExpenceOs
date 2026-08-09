from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users" , views.UserViewSet , basename="user")
router.register("departments" , views.DepartmentViewSet , basename="department")

urlpatterns = [
    path("login/" , views.LoginViewSet.as_view() , name="login"),
]

urlpatterns += router.urls