from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="inventory_dashboard"),
    path("view/", views.view_inventory, name="view_inventory"),
    path("stock-in/<int:id>/", views.stock_in, name="stock_in"),
    path("stock-out/<int:id>/", views.stock_out, name="stock_out"),
]