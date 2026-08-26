
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.db import transaction as db_transaction
from django.shortcuts import redirect, render

from .models import Account, Transaction, BankAdmin


# ============================================================
# USER ACCOUNT HELPER
# ============================================================

def get_user_account(request):
    account_id = request.session.get("atm_account_id")

    if not account_id:
        return None

    try:
        return Account.objects.get(id=account_id)
    except Account.DoesNotExist:
        request.session.flush()
        return None


# ============================================================
# USER LOGIN
# ============================================================

def user_login(request):

    # Already logged in
    if request.session.get("atm_account_id"):
        return redirect("user_dashboard")

    if request.method == "POST":

        account_number = request.POST.get(
            "account_number",
            ""
        ).strip()

        pin = request.POST.get(
            "pin",
            ""
        ).strip()

        if not account_number or not pin:

            messages.error(
                request,
                "Please enter account number and PIN."
            )

            return render(
                request,
                "atm/user_login.html"
            )

        try:
            account = Account.objects.get(
                account_number=account_number
            )

        except Account.DoesNotExist:

            messages.error(
                request,
                "Invalid account number or PIN."
            )

            return render(
                request,
                "atm/user_login.html"
            )

        # Check encrypted PIN
        if not account.check_pin(pin):

            messages.error(
                request,
                "Invalid account number or PIN."
            )

            return render(
                request,
                "atm/user_login.html"
            )

        # Create ATM session
        request.session["atm_account_id"] = account.id
        request.session["atm_account_number"] = (
            account.account_number
        )

        request.session.modified = True

        return redirect("user_dashboard")

    return render(
        request,
        "atm/user_login.html"
    )


# ============================================================
# USER LOGOUT
# ============================================================

def user_logout(request):

    request.session.pop(
        "atm_account_id",
        None
    )

    request.session.pop(
        "atm_account_number",
        None
    )

    messages.success(
        request,
        "You have logged out successfully."
    )

    return redirect("user_login")


# ============================================================
# USER DASHBOARD
# ============================================================

def user_dashboard(request):

    account = get_user_account(request)

    if not account:

        messages.warning(
            request,
            "Please login to your ATM account."
        )

        return redirect("user_login")

    recent_transactions = (
        Transaction.objects
        .filter(account=account)
        .order_by("-created_at")[:10]
    )

    total_transactions = (
        Transaction.objects
        .filter(account=account)
        .count()
    )

    deposits = (
        Transaction.objects
        .filter(
            account=account,
            transaction_type="DEPOSIT"
        )
    )

    withdrawals = (
        Transaction.objects
        .filter(
            account=account,
            transaction_type="WITHDRAW"
        )
    )

    total_deposits = sum(
        (item.amount for item in deposits),
        Decimal("0.00")
    )

    total_withdrawals = sum(
        (item.amount for item in withdrawals),
        Decimal("0.00")
    )

    context = {
        "account": account,
        "recent_transactions": recent_transactions,
        "total_transactions": total_transactions,
        "total_deposits": total_deposits,
        "total_withdrawals": total_withdrawals,
    }

    return render(
        request,
        "atm/user_dashboard.html",
        context
    )


# ============================================================
# DEPOSIT
# ============================================================

def deposit(request):

    account = get_user_account(request)

    if not account:
        return redirect("user_login")

    if request.method == "POST":

        amount_text = request.POST.get(
            "amount",
            ""
        ).strip()

        try:
            amount = Decimal(amount_text)

        except (InvalidOperation, ValueError):

            messages.error(
                request,
                "Enter a valid amount."
            )

            return render(
                request,
                "atm/deposit.html",
                {
                    "account": account
                }
            )

        if amount <= 0:

            messages.error(
                request,
                "Amount must be greater than zero."
            )

            return render(
                request,
                "atm/deposit.html",
                {
                    "account": account
                }
            )

        with db_transaction.atomic():

            account.balance += amount

            account.save(
                update_fields=["balance"]
            )

            Transaction.objects.create(
                account=account,
                transaction_type="DEPOSIT",
                amount=amount,
                description="ATM Cash Deposit"
            )

        messages.success(
            request,
            f"Deposit of {amount:,.2f} completed successfully."
        )

        return redirect("user_dashboard")

    return render(
        request,
        "atm/deposit.html",
        {
            "account": account
        }
    )


# ============================================================
# WITHDRAW
# ============================================================

def withdraw(request):

    account = get_user_account(request)

    if not account:
        return redirect("user_login")

    if request.method == "POST":

        amount_text = request.POST.get(
            "amount",
            ""
        ).strip()

        try:
            amount = Decimal(amount_text)

        except (InvalidOperation, ValueError):

            messages.error(
                request,
                "Enter a valid amount."
            )

            return render(
                request,
                "atm/withdraw.html",
                {
                    "account": account
                }
            )

        if amount <= 0:

            messages.error(
                request,
                "Amount must be greater than zero."
            )

            return render(
                request,
                "atm/withdraw.html",
                {
                    "account": account
                }
            )

        if amount > account.balance:

            messages.error(
                request,
                "Insufficient balance."
            )

            return render(
                request,
                "atm/withdraw.html",
                {
                    "account": account
                }
            )

        with db_transaction.atomic():

            account.balance -= amount

            account.save(
                update_fields=["balance"]
            )

            Transaction.objects.create(
                account=account,
                transaction_type="WITHDRAW",
                amount=amount,
                description="ATM Cash Withdrawal"
            )

        messages.success(
            request,
            f"Withdrawal of {amount:,.2f} completed successfully."
        )

        return redirect("user_dashboard")

    return render(
        request,
        "atm/withdraw.html",
        {
            "account": account
        }
    )


# ============================================================
# TRANSFER
# ============================================================

def transfer(request):

    account = get_user_account(request)

    if not account:
        return redirect("user_login")

    if request.method == "POST":

        destination_number = request.POST.get(
            "account_number",
            ""
        ).strip()

        amount_text = request.POST.get(
            "amount",
            ""
        ).strip()

        if not destination_number:

            messages.error(
                request,
                "Enter destination account number."
            )

            return render(
                request,
                "atm/transfer.html",
                {
                    "account": account
                }
            )

        try:
            amount = Decimal(amount_text)

        except (InvalidOperation, ValueError):

            messages.error(
                request,
                "Enter a valid amount."
            )

            return render(
                request,
                "atm/transfer.html",
                {
                    "account": account
                }
            )

        if amount <= 0:

            messages.error(
                request,
                "Amount must be greater than zero."
            )

            return render(
                request,
                "atm/transfer.html",
                {
                    "account": account
                }
            )

        if amount > account.balance:

            messages.error(
                request,
                "Insufficient balance."
            )

            return render(
                request,
                "atm/transfer.html",
                {
                    "account": account
                }
            )

        try:

            destination = Account.objects.get(
                account_number=destination_number
            )

        except Account.DoesNotExist:

            messages.error(
                request,
                "Destination account not found."
            )

            return render(
                request,
                "atm/transfer.html",
                {
                    "account": account
                }
            )

        if destination.id == account.id:

            messages.error(
                request,
                "You cannot transfer to your own account."
            )

            return render(
                request,
                "atm/transfer.html",
                {
                    "account": account
                }
            )

        with db_transaction.atomic():

            account.balance -= amount

            destination.balance += amount

            account.save(
                update_fields=["balance"]
            )

            destination.save(
                update_fields=["balance"]
            )

            Transaction.objects.create(
                account=account,
                transaction_type="TRANSFER",
                amount=amount,
                description=(
                    f"Transfer to "
                    f"{destination.account_number}"
                )
            )

            Transaction.objects.create(
                account=destination,
                transaction_type="TRANSFER",
                amount=amount,
                description=(
                    f"Transfer from "
                    f"{account.account_number}"
                )
            )

        messages.success(
            request,
            (
                f"Transfer of {amount:,.2f} "
                f"to {destination.account_number} "
                f"completed successfully."
            )
        )

        return redirect("user_dashboard")

    return render(
        request,
        "atm/transfer.html",
        {
            "account": account
        }
    )


# ============================================================
# USER TRANSACTION HISTORY
# ============================================================

def user_transactions(request):

    account = get_user_account(request)

    if not account:
        return redirect("user_login")

    transactions_list = (
        Transaction.objects
        .filter(account=account)
        .order_by("-created_at")
    )

    return render(
        request,
        "atm/user_transactions.html",
        {
            "account": account,
            "transactions": transactions_list,
        }
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

def admin_dashboard(request):

    total_accounts = Account.objects.count()

    total_transactions = Transaction.objects.count()

    total_bank_admins = BankAdmin.objects.count()

    accounts_list = Account.objects.all()

    total_balance = sum(
        (
            account.balance
            for account in accounts_list
        ),
        Decimal("0.00")
    )

    recent_transactions = (
        Transaction.objects
        .select_related("account")
        .order_by("-created_at")[:10]
    )

    context = {
        "total_accounts": total_accounts,
        "total_transactions": total_transactions,
        "total_bank_admins": total_bank_admins,
        "total_balance": total_balance,
        "recent_transactions": recent_transactions,
    }

    return render(
        request,
        "atm/admin_dashboard.html",
        context
    )


# ============================================================
# ADMIN ACCOUNTS
# ============================================================

def accounts(request):

    accounts_list = (
        Account.objects
        .order_by("-created_at")
    )

    return render(
        request,
        "atm/accounts.html",
        {
            "accounts": accounts_list
        }
    )


# ============================================================
# ADMIN TRANSACTIONS
# ============================================================

def transactions(request):

    transactions_list = (
        Transaction.objects
        .select_related("account")
        .order_by("-created_at")
    )

    return render(
        request,
        "atm/transactions.html",
        {
            "transactions": transactions_list
        }
    )


# ============================================================
# BANK ADMINS
# ============================================================

def bank_admins(request):

    bank_admins_list = (
        BankAdmin.objects
        .order_by("username")
    )

    return render(
        request,
        "atm/bank_admins.html",
        {
            "bank_admins": bank_admins_list
        }
    )
