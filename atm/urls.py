
from django.urls import path

from . import views


urlpatterns = [

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    path(
        "admin-dashboard/add-account/",
        views.add_account,
        name="add_account"
    ),

]
