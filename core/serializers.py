from rest_framework import serializers
from .models import User , Department
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["role"] = user.role
        token["employee_id"] = user.employee_id

        return token

class UserSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source="department.name", read_only=True, default=None)
    manager_name = serializers.CharField(source="manager.username", read_only=True, default=None)

    class Meta:
        model = User
        fields = ["id" , "username" , "email" , "employee_id" , "manager" , "manager_name" ,"department" , "department_name" , "role" , "is_active"]

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id" , "username" , "email" , "password" , "employee_id" , "department" , "manager" , "role" , "is_active"]

        extra_kwargs = {
            "password" : {"write_only" : True}
        }

    def create(self , validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

class DepartmentSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source="manager.username", read_only=True, default=None)
    spent = serializers.SerializerMethodField()
    class Meta:
        model = Department
        fields = ["id" , "name" , "code" , "description" , "manager" ,"manager_name", "is_active" , "spent"]
        
    def get_spent(self, obj):
        from django.db.models import Sum, Q
        from expenses.models import Expense
        total = Expense.objects.filter(
            Q(department=obj) | Q(employee__department=obj)
        ).exclude(
            status=Expense.Status.REJECTED
        ).distinct().aggregate(total=Sum("amount"))["total"]
        return float(total or 0)