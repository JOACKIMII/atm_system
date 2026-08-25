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
        .all()
        .order_by("-id")[:10]
    )

    recent_accounts = (
        Account.objects
        .all()
        .order_by("-id")[:10]
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