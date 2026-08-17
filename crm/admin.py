from django.contrib import admin
from .models import Enquiry


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):

    list_display = (
        "enquiry_no",
        "customer",
        "project_name",
        "city",
        "sales_executive",
        "expected_value",
        "lead_source",
        "status",
        "expected_closing_date",
    )

    list_filter = (
        "status",
        "lead_source",
        "city",
    )

    search_fields = (
        "enquiry_no",
        "project_name",
        "customer__customer_name",
        "sales_executive",
    )