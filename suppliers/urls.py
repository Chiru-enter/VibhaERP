from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="suppliers_dashboard"),
    path("add/", views.add_supplier, name="add_supplier"),
    path("view/", views.view_suppliers, name="view_suppliers"),
    path("edit/<int:id>/", views.edit_supplier, name="edit_supplier"),
    path("delete/<int:id>/", views.delete_supplier, name="delete_supplier"),
]