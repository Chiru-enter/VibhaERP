from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Inventory

def dashboard(request):
    return render(request, "inventory/dashboard.html")

def view_inventory(request):
    inventory = Inventory.objects.all()
    return render(
        request,
        "inventory/view_inventory.html",
        {"inventory": inventory}
    )

def stock_in(request, id):
    inventory = get_object_or_404(Inventory, id=id)

    if request.method == "POST":
        qty = int(request.POST["quantity"])

        inventory.quantity += qty
        inventory.save()

        messages.success(request, "Stock added successfully.")
        return redirect("view_inventory")

    return render(request, "inventory/stock_in.html", {"inventory": inventory})
def stock_out(request, id):
    inventory = get_object_or_404(Inventory, id=id)

    if request.method == "POST":
        qty = int(request.POST["quantity"])

        if qty > inventory.quantity:
            messages.error(request, "Not enough stock available.")
            return render(
                request,
                "inventory/stock_out.html",
                {"inventory": inventory}
            )

        inventory.quantity -= qty
        inventory.save()

        messages.success(request, "Stock removed successfully.")
        return redirect("view_inventory")

    return render(
        request,
        "inventory/stock_out.html",
        {"inventory": inventory}
    )