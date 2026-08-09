from django.shortcuts import render
from .models import User , Department
from .serializers import UserSerializer , UserCreateSerializer , DepartmentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from . import permissions

# Create your views here.

class UserViewSet(ModelViewSet):
    queryset = User.objects.select_related("department" , "manager").all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer

        return UserSerializer

    def get_permissions(self):
        if self.action in ["create" , "update" , "partial_update" , "destroy"]:
            return [permissions.IsAdmin()]

        return [IsAuthenticated()]

class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.select_related("manager").all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.action in ["create" , "update" , "partial_update" , "destroy"]:
            return [permissions.IsAdminReadOnly()]

        return [IsAuthenticated()]