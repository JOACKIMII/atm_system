from django.contrib import admin

from .models import Account, Transaction, BankAdmin


# =========================================================
# ACCOUNT ADMIN
# =========================================================

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):

    list_display = (
        "account_number",
        "full_name",
        "balance",
        "created_at",
    )

    search_fields = (
        "account_number",
        "full_name",
    )

    list_filter = (
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Customer Information",
            {
                "fields": (
                    "account_number",
                    "full_name",
                )
            },
        ),

        (
            "Security",
            {
                "fields": (
                    "pin",
                )
            },
        ),

        (
            "Account Balance",
            {
                "fields": (
                    "balance",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):

        # Kama account ni mpya
        if not change:

            raw_pin = obj.pin

            if raw_pin:
                obj.set_pin(raw_pin)

        # Kama account iliyopo imebadilishwa
        else:

            old_account = Account.objects.get(
                pk=obj.pk
            )

            # Kama PIN imebadilishwa,
            # hash PIN mpya
            if obj.pin != old_account.pin:

                obj.set_pin(obj.pin)

        super().save_model(
            request,
            obj,
            form,
            change
        )


# =========================================================
# TRANSACTION ADMIN
# =========================================================

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = (
        "account",
        "transaction_type",
        "amount",
        "description",
        "created_at",
    )

    search_fields = (
        "account__account_number",
        "account__full_name",
        "description",
    )

    list_filter = (
        "transaction_type",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )


# =========================================================
# BANK ADMIN
# =========================================================

@admin.register(BankAdmin)
class BankAdminAdmin(admin.ModelAdmin):

    list_display = (
        "username",
        "full_name",
    )

    search_fields = (
        "username",
        "full_name",
    )

    fieldsets = (
        (
            "Administrator Information",
            {
                "fields": (
                    "username",
                    "full_name",
                )
            },
        ),

        (
            "Security",
            {
                "fields": (
                    "password",
                )
            },
        ),
    )

    def save_model(self, request, obj, form, change):

        if not change:

            raw_password = obj.password

            if raw_password:
                obj.set_password(raw_password)

        else:

            old_admin = BankAdmin.objects.get(
                pk=obj.pk
            )

            if obj.password != old_admin.password:

                obj.set_password(
                    obj.password
                )

        super().save_model(
            request,
            obj,
            form,
            change
        )