from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="sales_dashboard"),

    path("new/", views.new_sale, name="new_sale"),

    path("history/", views.sales_history, name="sales_history"),

    path(
        "invoice/<int:id>/",
        views.invoice_details,
        name="invoice_details",
    ),

    path(
        "invoice/<int:id>/add-item/",
        views.add_item,
        name="add_item",
    ),

    # ==========================
    # Receive Payment
    # ==========================

    path(
        "invoice/<int:id>/receive-payment/",
        views.receive_payment,
        name="receive_payment",
    ),
]