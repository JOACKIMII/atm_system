from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from .models import Account, Transaction, BankAdmin


@login_required
def admin_dashboard(request):
    total_accounts = Account.objects.count()
    total_transactions = Transaction.objects.count()
    total_admins = BankAdmin.objects.count()

    total_balance = (
        Account.objects.aggregate(total=Sum("balance"))["total"] or 0
    )

    recent_transactions = (
        Transaction.objects
        .select_related("account")
        .order_by("-created_at")[:10]
    )

    recent_accounts = (
        Account.objects
        .order_by("-created_at")[:10]
    )

    context = {
        "total_accounts": total_accounts,
        "total_transactions": total_transactions,
        "total_admins": total_admins,
        "total_balance": total_balance,
        "recent_transactions": recent_transactions,
        "recent_accounts": recent_accounts,
    }

    return render(
        request,
        "atm/admin_dashboard.html",
        context
    )


@login_required
def accounts(request):
    accounts_list = Account.objects.order_by("-created_at")

    total_accounts = accounts_list.count()

    total_balance = (
        accounts_list.aggregate(total=Sum("balance"))["total"] or 0
    )

    context = {
        "accounts": accounts_list,
        "total_accounts": total_accounts,
        "active_accounts": total_accounts,
        "total_balance": total_balance,
    }

    return render(
        request,
        "atm/accounts.html",
        context
    )


@login_required
def transactions(request):
    transactions_list = (
        Transaction.objects
        .select_related("account")
        .order_by("-created_at")
    )

    total_transactions = transactions_list.count()

    total_deposits = (
        transactions_list
        .filter(transaction_type="DEPOSIT")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    total_withdrawals = (
        transactions_list
        .filter(transaction_type="WITHDRAW")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    total_transfers = (
        transactions_list
        .filter(transaction_type="TRANSFER")
        .aggregate(total=Sum("amount"))["total"] or 0
    )

    context = {
        "transactions": transactions_list,
        "total_transactions": total_transactions,
        "total_deposits": total_deposits,
        "total_withdrawals": total_withdrawals,
        "total_transfers": total_transfers,
    }

    return render(
        request,
        "atm/transactions.html",
        context
    )


@login_required
def bank_admins(request):
    admins = BankAdmin.objects.order_by("username")

    total_admins = admins.count()

    context = {
        "bank_admins": admins,
        "admins": admins,
        "total_admins": total_admins,
    }

    return render(
        request,
        "atm/bank_admins.html",
        context
    )