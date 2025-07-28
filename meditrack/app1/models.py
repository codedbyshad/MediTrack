from django.db import models
from django.utils import timezone

# ---------------------------------------
# User Login Model
# ---------------------------------------
class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    def __str__(self):
        return self.username


# ---------------------------------------
# Medicine Management Model
# ---------------------------------------
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name

# ---------------------------------------
# Customer Model
# ---------------------------------------


class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.name} ({self.phone})"


# ---------------------------------------
# Sales Model
# ---------------------------------------


class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    sale_data = models.JSONField()
    created_at = models.DateTimeField(default=timezone.now)
    invoice_number = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Sale to {self.customer.name} on {self.created_at.strftime('%Y-%m-%d')} (Invoice #{self.invoice_number})"
