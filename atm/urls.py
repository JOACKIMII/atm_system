from django.urls import path
from . import views


urlpatterns = [
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