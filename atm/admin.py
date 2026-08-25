
from django.contrib import admin
from .models import Account, Transaction, BankAdmin


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "account_number",
        "balance",
    )

    search_fields = (
        "account_number",
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "account",
        "amount",
    )

    search_fields = (
        "account__account_number",
    )


@admin.register(BankAdmin)
class BankAdminAdmin(admin.ModelAdmin):
    list_display = (
        "id",
    )

