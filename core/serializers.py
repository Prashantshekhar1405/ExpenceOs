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
    class Meta:
        model = User
        fields = ["id" , "username" , "email" , "employee_id" , "manager" ,"department" , "role"]

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username" , "email" , "password" , "employee_id" , "department" , "manager" , "role"]

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
    class Meta:
        model = Department
        fields = ["id" , "name" , "code" , "description" , "manager" , "is_active"]