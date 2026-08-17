from django.urls import path
from . import views


urlpatterns = [

    path(
        "",
        views.dashboard,
        name="crm_dashboard"
    ),

    path(
        "new/",
        views.new_enquiry,
        name="crm_new_enquiry"
    ),

    path(
        "enquiry/<int:id>/",
        views.enquiry_details,
        name="crm_enquiry_details"
    ),

    path(
        "enquiry/<int:id>/edit/",
        views.edit_enquiry,
        name="crm_edit_enquiry"
    ),
]