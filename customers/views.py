from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from django.contrib import messages



def dashboard(request):
    return render(request, "customers/dashboard.html")


def add_customer(request):
    if request.method == "POST":

        customer_id = request.POST["customer_id"]

        if Customer.objects.filter(customer_id=customer_id).exists():
            messages.error(request, "Customer ID already exists.")
            return render(request, "customers/add_customer.html")

        Customer.objects.create(
            customer_id=customer_id,
            customer_name=request.POST["customer_name"],
            contact_person=request.POST["contact_person"],
            phone=request.POST["phone"],
            email=request.POST["email"],
            address=request.POST["address"],
        )

        messages.success(request, "Customer added successfully.")
        return redirect("view_customers")

    return render(request, "customers/add_customer.html")


def view_customers(request):
    customers = Customer.objects.all()
    return render(request, "customers/view_customers.html", {"customers": customers})


def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == "POST":
        customer.customer_id = request.POST["customer_id"]
        customer.customer_name = request.POST["customer_name"]
        customer.contact_person = request.POST["contact_person"]
        customer.phone = request.POST["phone"]
        customer.email = request.POST["email"]
        customer.address = request.POST["address"]
        customer.save()

        return redirect("view_customers")

    return render(request, "customers/edit_customer.html", {"customer": customer})


def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)
    customer.delete()
    return redirect("view_customers")
