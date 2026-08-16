from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = [
            "id" , "employee" ,"employee_name", 
            "expense_category" ,"expense_category_name", 
            "amount" , "department" ,"department_name", 
            "expense_date" , "reason" , "status"
        ]
        read_only_fields = ["id" , "employee" , "status"]

        def get_department_name(self, obj):
            return obj.department.name if obj.department else None

        def get_expense_category_name(self, obj):
            return obj.expense_category.name if obj.expense_category else None

        def get_employee_name(self, obj):
            return obj.employee.username if obj.employee else None
