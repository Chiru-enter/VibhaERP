from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.dashboard,
        name="purchase_dashboard"
    ),

    path(
        "new/",
        views.new_purchase,
        name="new_purchase"
    ),

    path(
        "history/",
        views.purchase_history,
        name="purchase_history"
    ),

    path(
        "invoice/<int:id>/",
        views.purchase_details,
        name="purchase_details"
    ),

    path(
        "invoice/<int:id>/add-item/",
        views.add_item,
        name="purchase_add_item"
    ),

    path(
        "invoice/<int:id>/make-payment/",
        views.make_payment,
        name="make_payment"
    ),

]