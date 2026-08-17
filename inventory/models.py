from django.db import models
from products.models import Product


class Inventory(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=0)

    reorder_level = models.PositiveIntegerField(default=10)

    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity}"
