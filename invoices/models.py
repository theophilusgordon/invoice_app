from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_photo_url = models.CharField(max_length=500)
    phone = models.CharField(max_length=15)
    is_staff = models.BooleanField(default=False)

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"
    
class Item(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (x{self.quantity})"

class Invoice(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]

    id = models.CharField(max_length=20, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    payment_due = models.DateField()
    description = models.TextField()
    payment_terms = models.PositiveIntegerField()
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    sender_address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='sender_invoices')
    client_address = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='client_invoices')
    items = models.ManyToManyField(Item, related_name='invoices')
    total = models.DecimalField(max_digits=15, decimal_places=2)

    def calculate_total(self):
        """Calculate and update the invoice total."""
        self.total = sum(item.total for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Invoice {self.id} - {self.status.capitalize()}"
