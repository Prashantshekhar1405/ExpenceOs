from rest_framework import serializers
from .models import Receipt
from core.models import User


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ["id" , "expense" , "file" , "uploaded_at"]
        read_only_fields = ["id" , "uploaded_at"]

    def validate_expense(self, expense):
        request = self.context["request"]
        user = request.user

        if user.role == User.Role.EMPLOYEE:
            if expense.employee != user:
                raise serializers.ValidationError(
                    "You can only upload receipts for your own expenses."
                )

        return expense
            

        