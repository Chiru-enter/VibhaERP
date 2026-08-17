from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier
from django.contrib import messages


def dashboard(request):
    return render(request, "suppliers/dashboard.html")


from django.contrib import messages

def add_supplier(request):
    if request.method == "POST":

        supplier_id = request.POST["supplier_id"]

        if Supplier.objects.filter(supplier_id=supplier_id).exists():
            messages.error(request, "Supplier ID already exists.")
            return render(request, "suppliers/add_supplier.html")

        Supplier.objects.create(
            supplier_id=supplier_id,
            supplier_name=request.POST["supplier_name"],
            contact_person=request.POST["contact_person"],
            phone=request.POST["phone"],
            email=request.POST["email"],
            address=request.POST["address"],
        )

        messages.success(request, "Supplier added successfully.")
        return redirect("view_suppliers")

    return render(request, "suppliers/add_supplier.html")


def view_suppliers(request):
    suppliers = Supplier.objects.all()
    print(suppliers)   # Temporary debug

    return render(
        request,
        "suppliers/view_suppliers.html",
        {
            "suppliers": suppliers
        }
    )

def edit_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)

    if request.method == "POST":
        supplier.supplier_id = request.POST["supplier_id"]
        supplier.supplier_name = request.POST["supplier_name"]
        supplier.contact_person = request.POST["contact_person"]
        supplier.phone = request.POST["phone"]
        supplier.email = request.POST["email"]
        supplier.address = request.POST["address"]
        supplier.save()

        return redirect("view_suppliers")

    return render(request, "suppliers/edit_supplier.html", {"supplier": supplier})


def delete_supplier(request, id):
    supplier = get_object_or_404(Supplier, id=id)
    supplier.delete()
    return redirect("view_suppliers")
