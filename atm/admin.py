from django.contrib import admin

from .models import Account, Transaction


# =========================================================
# ACCOUNT ADMIN
# =========================================================

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):

    list_display = (
        'account_number',
        'full_name',
        'balance',
        'created_at',
    )

    search_fields = (
        'account_number',
        'full_name',
    )

    list_filter = (
        'created_at',
    )

    readonly_fields = (
        'created_at',
    )


# =========================================================
# TRANSACTION ADMIN
# =========================================================

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        'account',
        'transaction_type',
        'amount',
        'description',
        'created_at',
    )

    search_fields = (
        'account__account_number',
        'account__full_name',
        'description',
    )

    list_filter = (
        'transaction_type',
        'created_at',
    )

    readonly_fields = (
        'created_at',
    )