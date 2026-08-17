from django.db import models
from decimal import Decimal
from customers.models import Customer
from products.models import Product


class Sale(models.Model):
    invoice_no = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sale_date = models.DateField(auto_now_add=True)

    # Financial Details
    sub_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    cgst_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=9
    )

    sgst_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=9
    )

    cgst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    sgst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    grand_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # Temporary compatibility
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # Payment
    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    balance_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Partial", "Partial"),
        ("Paid", "Paid"),
    ]

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    def calculate_totals(self):
        self.cgst_amount = (
            self.sub_total * self.cgst_rate
        ) / Decimal("100")

        self.sgst_amount = (
            self.sub_total * self.sgst_rate
        ) / Decimal("100")

        self.grand_total = (
            self.sub_total
            + self.cgst_amount
            + self.sgst_amount
        )

        self.total_amount = self.grand_total

        self.balance_amount = (
            self.grand_total
            - self.paid_amount
        )

        if self.balance_amount <= 0:
            self.balance_amount = Decimal("0.00")
            self.payment_status = "Paid"
        elif self.paid_amount == 0:
            self.payment_status = "Pending"
        else:
            self.payment_status = "Partial"

    def __str__(self):
        return self.invoice_no


class SaleItem(models.Model):
    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.product_name


# ======================================================
# PAYMENT HISTORY
# ======================================================

class SalePayment(models.Model):

    PAYMENT_MODES = [
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Card", "Card"),
        ("Bank Transfer", "Bank Transfer"),
    ]

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    payment_date = models.DateTimeField(auto_now_add=True)

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODES
    )

    remarks = models.CharField(
        max_length=200,
        blank=True
    )

    def __str__(self):
        return f"{self.sale.invoice_no} - ₹{self.amount}"