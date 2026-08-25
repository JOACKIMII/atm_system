from django.urls import path
from . import views


urlpatterns = [

    # ==============================
    # HOME
    # ==============================

    path(
        '',
        views.home,
        name='home'
    ),

    # ==============================
    # CUSTOMER LOGIN
    # ==============================

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    # ==============================
    # CUSTOMER LOGOUT
    # ==============================

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # ==============================
    # DASHBOARD
    # ==============================

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # ==============================
    # WITHDRAW
    # ==============================

    path(
        'withdraw/',
        views.withdraw,
        name='withdraw'
    ),

    # ==============================
    # DEPOSIT
    # ==============================

    path(
        'deposit/',
        views.deposit,
        name='deposit'
    ),

    # ==============================
    # TRANSACTIONS
    # ==============================

    path(
        'transactions/',
        views.transactions,
        name='transactions'
    ),

    # ==============================
    # EXPLORE
    # ==============================

    path(
        'explore/',
        views.explore,
        name='explore'
    ),

]