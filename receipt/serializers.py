from rest_framework import serializers
from .models import Receipt
from core.models import User


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ["id" , "expense" , "file" , "uploaded_at" , "ocr_status" , "merchant" , "receipt_amount" , "receipt_date" , "tax_amount" , "invoice_number"]
        read_only_fields = ["id" , "uploaded_at" ,  "ocr_status" , "merchant" , "receipt_amount" , "receipt_date" , "tax_amount" , "invoice_number"]

    def validate_expense(self, expense):
        request = self.context["request"]
        user = request.user

        if user.role == User.Role.EMPLOYEE:
            if expense.employee != user:
                raise serializers.ValidationError(
                    "You can only upload receipts for your own expenses."
                )

        return expense

    def validate_file(self , file):
        max_size = 2 * 1024 * 1024
        if file.size > max_size:
            raise serializers.ValidationError(
                "Receipt file must be less then 2MB"
            )

        allowed_types = [
            "image/jpeg",
            "image/png",
        ]

        if file.content_type not in allowed_types:
            raise serializers.ValidationError(
                "only jpg png and pdfs are allowed"
            )
        return file
    
        