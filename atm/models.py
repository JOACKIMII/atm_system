from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Account(models.Model):

    account_number = models.CharField(
        max_length=20,
        unique=True
    )

    full_name = models.CharField(
        max_length=100
    )

    pin = models.CharField(
        max_length=128
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def set_pin(self, raw_pin):
        self.pin = make_password(raw_pin)

    def check_pin(self, raw_pin):
        return check_password(raw_pin, self.pin)

    def __str__(self):
        return f"{self.account_number} - {self.full_name}"


class Transaction(models.Model):

    TRANSACTION_TYPES = [
        ('DEPOSIT', 'Deposit'),
        ('WITHDRAW', 'Withdraw'),
        ('TRANSFER', 'Transfer'),
    ]

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    description = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.account.account_number} - "
            f"{self.transaction_type} - "
            f"{self.amount}"
        )


class BankAdmin(models.Model):

    username = models.CharField(
        max_length=50,
        unique=True
    )

    full_name = models.CharField(
        max_length=100
    )

    password = models.CharField(
        max_length=128
    )

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(
            raw_password,
            self.password
        )

    def __str__(self):
        return self.username