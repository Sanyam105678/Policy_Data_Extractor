from django.contrib import admin
from .models import Policy


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):

    # What to show in Policy table
    list_display = (
        "id",
        "insured_name",
        "insurance_company_name",
        "policy_sub_type",
        "registration_number",
        "start_date",
        "end_date",
        "gross_premium",
        "status",
        "created_at",
    )

    # Filters on right side
    list_filter = (
        "insurance_company_name",
        "policy_sub_type",
        "status",
        "start_date",
        "end_date",
        "created_at",
    )

    # Search bar fields
    search_fields = (
        "insured_name",
        "insured_email",
        "insured_mobile",
        "registration_number",
        "engine_number",
        "chassis_number",
    )

    # Which fields are clickable to open the detail view
    list_display_links = ("id", "insured_name", "registration_number")

    # Default ordering
    ordering = ("-created_at",)




    