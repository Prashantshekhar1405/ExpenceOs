from rest_framework import serializers
from .models import Reimbursement

class ReimbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reimbursement
        fields = [
            "id",
            "expense",
            "employee",
            "amount",
            "status",
            "processed_by",
            "processed_at",
            "transaction_reference",
            "failure_reason",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "employee",
            "expense",
            "amount",
            "status",
            "processed_by",
            "processed_at",
            "created_at",
            "updated_at",
        ]