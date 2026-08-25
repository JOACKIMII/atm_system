from decimal import Decimal, InvalidOperation

from django.shortcuts import render, redirect

from .models import Account, Transaction


# =========================================================
# HOME
# =========================================================

def home(request):
    return render(
        request,
        'atm/home.html'
    )


# =========================================================
# CUSTOMER LOGIN
# =========================================================

def login_view(request):

    if request.session.get('account_id'):
        return redirect('dashboard')

    error = None

    if request.method == 'POST':

        account_number = request.POST.get(
            'account_number',
            ''
        ).strip()

        pin = request.POST.get(
            'pin',
            ''
        ).strip()

        try:

            account = Account.objects.get(
                account_number=account_number,
                pin=pin
            )

            request.session['account_id'] = account.id

            return redirect('dashboard')

        except Account.DoesNotExist:

            error = 'Invalid account number or PIN.'

    return render(
        request,
        'atm/login.html',
        {
            'error': error
        }
    )


# =========================================================
# CUSTOMER LOGOUT
# =========================================================

def logout_view(request):

    request.session.flush()

    return redirect('login')


# =========================================================
# DASHBOARD
# =========================================================

def dashboard(request):

    account_id = request.session.get(
        'account_id'
    )

    if not account_id:
        return redirect('login')

    try:

        account = Account.objects.get(
            id=account_id
        )

    except Account.DoesNotExist:

        request.session.flush()

        return redirect('login')

    return render(
        request,
        'atm/dashboard.html',
        {
            'account': account
        }
    )


# =========================================================
# WITHDRAW
# =========================================================

def withdraw(request):

    account_id = request.session.get(
        'account_id'
    )

    if not account_id:
        return redirect('login')

    try:

        account = Account.objects.get(
            id=account_id
        )

    except Account.DoesNotExist:

        request.session.flush()

        return redirect('login')

    error = None
    success = None

    if request.method == 'POST':

        amount_text = request.POST.get(
            'amount',
            ''
        ).strip()

        try:

            amount = Decimal(
                amount_text
            )

            if amount <= 0:

                error = (
                    'Please enter a valid amount.'
                )

            elif amount > account.balance:

                error = (
                    'Insufficient balance.'
                )

            else:

                account.balance -= amount

                account.save(
                    update_fields=['balance']
                )

                Transaction.objects.create(
                    account=account,
                    transaction_type='WITHDRAW',
                    amount=amount,
                    description='Cash withdrawal'
                )

                success = (
                    f'Withdrawal of TSh '
                    f'{amount:,.2f} was successful.'
                )

        except (
            InvalidOperation,
            ValueError,
            TypeError
        ):

            error = (
                'Please enter a valid amount.'
            )

    return render(
        request,
        'atm/withdraw.html',
        {
            'account': account,
            'error': error,
            'success': success
        }
    )


# =========================================================
# DEPOSIT
# =========================================================

def deposit(request):

    account_id = request.session.get(
        'account_id'
    )

    if not account_id:
        return redirect('login')

    try:

        account = Account.objects.get(
            id=account_id
        )

    except Account.DoesNotExist:

        request.session.flush()

        return redirect('login')

    error = None
    success = None

    if request.method == 'POST':

        amount_text = request.POST.get(
            'amount',
            ''
        ).strip()

        try:

            amount = Decimal(
                amount_text
            )

            if amount <= 0:

                error = (
                    'Please enter a valid amount.'
                )

            else:

                account.balance += amount

                account.save(
                    update_fields=['balance']
                )

                Transaction.objects.create(
                    account=account,
                    transaction_type='DEPOSIT',
                    amount=amount,
                    description='Cash deposit'
                )

                success = (
                    f'Deposit of TSh '
                    f'{amount:,.2f} was successful.'
                )

        except (
            InvalidOperation,
            ValueError,
            TypeError
        ):

            error = (
                'Please enter a valid amount.'
            )

    return render(
        request,
        'atm/deposit.html',
        {
            'account': account,
            'error': error,
            'success': success
        }
    )


# =========================================================
# TRANSACTIONS
# =========================================================

def transactions(request):

    account_id = request.session.get(
        'account_id'
    )

    if not account_id:
        return redirect('login')

    try:

        account = Account.objects.get(
            id=account_id
        )

    except Account.DoesNotExist:

        request.session.flush()

        return redirect('login')

    transaction_list = (
        Transaction.objects
        .filter(account=account)
        .order_by('-created_at')
    )

    return render(
        request,
        'atm/transactions.html',
        {
            'account': account,
            'transactions': transaction_list
        }
    )


# =========================================================
# EXPLORE SERVICES
# =========================================================

def explore(request):

    account_id = request.session.get(
        'account_id'
    )

    if not account_id:
        return redirect('login')

    try:

        account = Account.objects.get(
            id=account_id
        )

    except Account.DoesNotExist:

        request.session.flush()

        return redirect('login')

    return render(
        request,
        'atm/explore.html',
        {
            'account': account
        }
    )