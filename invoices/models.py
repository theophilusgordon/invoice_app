from django.db import models

from auth_app.models import Address
from items_app.models import Item

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
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def calculate_total(self):
        self.total = sum(item.total for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Invoice {self.id} - {self.status.capitalize()}"
