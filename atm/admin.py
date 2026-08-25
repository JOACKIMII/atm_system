from django.contrib import admin
from django import forms

from .models import Account, Transaction, BankAdmin


# =========================================================
# ACCOUNT FORM
# =========================================================

class AccountAdminForm(forms.ModelForm):

    pin = forms.CharField(
        label='PIN',
        widget=forms.PasswordInput(
            render_value=False
        ),
        max_length=20,
        required=True
    )

    class Meta:
        model = Account
        fields = (
            'account_number',
            'full_name',
            'pin',
            'balance',
        )

    def save(self, commit=True):

        account = super().save(
            commit=False
        )

        raw_pin = self.cleaned_data['pin']

        # Hash the PIN before saving
        account.set_pin(raw_pin)

        if commit:
            account.save()

        return account


# =========================================================
# ACCOUNT ADMIN
# =========================================================

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):

    form = AccountAdminForm

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


# =========================================================
# BANK ADMIN
# =========================================================

@admin.register(BankAdmin)
class BankAdminAdmin(admin.ModelAdmin):

    list_display = (
        'username',
        'full_name',
    )

    search_fields = (
        'username',
        'full_name',
    )