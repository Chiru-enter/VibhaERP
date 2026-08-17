from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="customers_dashboard"),
    path("add/", views.add_customer, name="add_customer"),
    path("view/", views.view_customers, name="view_customers"),
    path("edit/<int:id>/", views.edit_customer, name="edit_customer"),
    path("delete/<int:id>/", views.delete_customer, name="delete_customer"),
]