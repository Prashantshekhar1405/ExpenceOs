from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , Department
# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "employee_id",
        "role",
        "department",
        "manager",
        "is_active",
    )

    search_fields = (
        "email",
        "employee_id",
        "username",
    )

    ordering = ("email",)
    
    fieldsets = UserAdmin.fieldsets + (
        (
            "ExpenseOs Information" ,
            {
                "fields" : (
                    "employee_id",
                    "department",
                    "manager",
                    "role",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "ExpenseOS Information",
            {
                "fields": (
                    "email",
                    "employee_id",
                    "department",
                    "manager",
                    "role",
                )
            },
        ),
    )

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "code",
        "manager",
        "is_active",
    )
