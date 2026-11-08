from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("customers/", views.customer_list, name="customer_list"),
    path("customers/add/", views.customer_add, name="customer_add"),
    path("customers/<int:pk>/", views.customer_detail, name="customer_detail"),
    path("sales/add/", views.sale_add, name="sale_add"),
    path("payments/add/", views.payment_add, name="payment_add"),
    path("stock/", views.stock_list, name="stock_list"),
    path("reports/", views.reports, name="reports"),
    path("backup/", views.backup_json, name="backup"),
]
