from django.contrib import admin
from .models import Reimbursement


@admin.register(Reimbursement)
class ReimbursementAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "expense",
        "employee",
        "amount",
        "status",
        "processed_by",
        "processed_at",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
        "processed_at",
    )

    search_fields = (
        "employee__email",
        "employee__first_name",
        "employee__last_name",
        "transaction_reference",
        "expense__id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-created_at",
    )