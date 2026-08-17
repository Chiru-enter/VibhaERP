from django.db import models

class Customer(models.Model):
    customer_id = models.CharField(max_length=20, unique=True)
    customer_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.customer_name
