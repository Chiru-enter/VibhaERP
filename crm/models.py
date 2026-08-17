from django.db import models
from customers.models import Customer


class Enquiry(models.Model):

    LEAD_SOURCES = [
        ("Website", "Website"),
        ("Dealer", "Dealer"),
        ("Architect", "Architect"),
        ("Tender", "Tender"),
        ("Walk-in", "Walk-in"),
    ]

    STATUS_CHOICES = [
        ("New", "New"),
        ("Follow-up", "Follow-up"),
        ("Quotation", "Quotation"),
        ("Won", "Won"),
        ("Lost", "Lost"),
    ]

    enquiry_no = models.CharField(
        max_length=20,
        unique=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="enquiries"
    )

    company = models.CharField(
        max_length=150,
        blank=True
    )

    contact_person = models.CharField(
        max_length=100,
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    project_name = models.CharField(
        max_length=200
    )

    sales_executive = models.CharField(
        max_length=100,
        blank=True
    )

    expected_value = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        default=0
    )

    expected_closing_date = models.DateField(
        null=True,
        blank=True
    )

    lead_source = models.CharField(
        max_length=30,
        choices=LEAD_SOURCES,
        default="Website"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New"
    )

    notes = models.TextField(
        blank=True
    )

    drawing = models.FileField(
        upload_to="crm/drawings/",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.enquiry_no} - {self.project_name}"