from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="reports_dashboard"),
    path("sales/", views.sales_report, name="sales_report"),
    path("purchase/", views.purchase_report, name="purchase_report"),
    path("inventory/", views.inventory_report, name="inventory_report"),
    path("sales/pdf/", views.sales_pdf, name="sales_pdf"),
    path("purchase/pdf/", views.purchase_pdf, name="purchase_pdf"),
    path("inventory/pdf/", views.inventory_pdf, name="inventory_pdf"),
]