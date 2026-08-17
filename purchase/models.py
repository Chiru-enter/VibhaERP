from decimal import Decimal

from django.db import models

from suppliers.models import Supplier
from products.models import Product


class Purchase(models.Model):

    purchase_no = models.CharField(
        max_length=20,
        unique=True
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE
    )

    purchase_date = models.DateField(
        auto_now_add=True
    )

    # Amount Details

    sub_total = models.DecimalField(
        max_digits=10,
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
        max_digits=10,
        decimal_places=2,
        default=0
    )

    sgst_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    grand_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Keep temporarily for compatibility
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # Payment Details

    paid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    balance_amount = models.DecimalField(
        max_digits=10,
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
            self.sub_total +
            self.cgst_amount +
            self.sgst_amount
        )

        # Compatibility with existing reports
        self.total_amount = self.grand_total

        self.balance_amount = (
            self.grand_total -
            self.paid_amount
        )

        if self.balance_amount <= 0:
            self.balance_amount = Decimal("0.00")
            self.payment_status = "Paid"

        elif self.paid_amount > 0:
            self.payment_status = "Partial"

        else:
            self.payment_status = "Pending"

    def __str__(self):
        return self.purchase_no


class PurchaseItem(models.Model):

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.product_name


class PurchasePayment(models.Model):

    PAYMENT_MODES = [
        ("Cash", "Cash"),
        ("UPI", "UPI"),
        ("Card", "Card"),
        ("Bank Transfer", "Bank Transfer"),
    ]

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_mode = models.CharField(
        max_length=30,
        choices=PAYMENT_MODES
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.purchase.purchase_no} - ₹{self.amount}"