from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="products_dashboard"),
    path("add/", views.add_product, name="add_product"),
    path("view/", views.view_products, name="view_products"),
    path("edit/<int:id>/", views.edit_product, name="edit_product"),
    path("delete/<int:id>/", views.delete_product, name="delete_product"),
]