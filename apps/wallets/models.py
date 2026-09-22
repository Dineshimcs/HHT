from decimal import Decimal
from django.db import models
from django.conf import settings
from drivers.models import DriverProfile

class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet ({self.user.username}): ₹{self.balance}"

class WalletTransaction(models.Model):
    class TxType(models.TextChoices):
        CREDIT = 'CREDIT', 'Credit'
        DEBIT = 'DEBIT', 'Debit'

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tx_type = models.CharField(max_length=10, choices=TxType.choices)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tx_type} ₹{self.amount} - {self.description}"

class DriverPayout(models.Model):
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='PENDING') # PENDING, PROCESSED
    created_at = models.DateTimeField(auto_now_add=True)
