from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id" , "employee" , "expense_category" , "amount" , "department" , "expense_date" , "reason" , "status"]
        read_only_fields = ["id" , "employee" , "status"]