from django.db import models

class Supplier(models.Model):
    supplier_id = models.CharField(max_length=20, unique=True)
    supplier_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.supplier_name
