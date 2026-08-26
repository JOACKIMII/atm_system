
from django.urls import path
from . import views


urlpatterns = [
    # USER ATM LOGIN
    path("", views.user_login, name="user_login"),
    path("login/", views.user_login, name="login"),

    # USER DASHBOARD
    path("dashboard/", views.user_dashboard, name="user_dashboard"),
    path("logout/", views.user_logout, name="user_logout"),

    # TRANSACTIONS
    path("deposit/", views.deposit, name="deposit"),
    path("withdraw/", views.withdraw, name="withdraw"),
    path("transfer/", views.transfer, name="transfer"),
    path(
        "my-transactions/",
        views.user_transactions,
        name="user_transactions"
    ),

    # ADMIN DASHBOARD
    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),
    path(
        "accounts/",
        views.accounts,
        name="accounts"
    ),
    path(
        "transactions/",
        views.transactions,
        name="transactions"
    ),
    path(
        "bank-admins/",
        views.bank_admins,
        name="bank_admins"
    ),
]
