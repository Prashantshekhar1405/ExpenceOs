from rest_framework import serializers
from .models import User , Department

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
        fields = ["name" , "code" , "description" , "manager" , "is_active"]