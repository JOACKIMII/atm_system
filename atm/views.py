
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.contrib import messages

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


@login_required
def add_account(request):
    if request.method == "POST":

        account_number = request.POST.get("account_number", "").strip()
        full_name = request.POST.get("full_name", "").strip()
        pin = request.POST.get("pin", "").strip()
        balance = request.POST.get("balance", "0").strip()

        if not account_number or not full_name or not pin:
            messages.error(
                request,
                "Please fill in all required fields."
            )

            return redirect("add_account")

        if Account.objects.filter(
            account_number=account_number
        ).exists():

            messages.error(
                request,
                f"Account {account_number} already exists."
            )

            return redirect("add_account")

        if len(pin) < 4:
            messages.error(
                request,
                "PIN must contain at least 4 digits."
            )

            return redirect("add_account")

        if not pin.isdigit():
            messages.error(
                request,
                "PIN must contain numbers only."
            )

            return redirect("add_account")

        try:
            account = Account(
                account_number=account_number,
                full_name=full_name,
                balance=balance
            )

            account.set_pin(pin)
            account.save()

            messages.success(
                request,
                f"Account {account_number} created successfully."
            )

            return redirect("admin_dashboard")

        except Exception as e:
            messages.error(
                request,
                f"Unable to create account: {e}"
            )

            return redirect("add_account")

    return render(
        request,
        "atm/add_account.html"
    )
