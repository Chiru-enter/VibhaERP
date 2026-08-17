from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.contrib import messages
from inventory.models import Inventory


def dashboard(request):
    return render(request, "products/dashboard.html")


def add_product(request):
    if request.method == "POST":

        product_id = request.POST["product_id"]

        if Product.objects.filter(product_id=product_id).exists():
            messages.error(request, "Product ID already exists.")
            return render(request, "products/add_product.html")

        product = Product.objects.create(
            product_id=request.POST["product_id"],
            product_name=request.POST["product_name"],
            price=request.POST["price"],
            quantity=request.POST["quantity"],
        )

        Inventory.objects.create(
    product=product,
    quantity=request.POST["quantity"],
    reorder_level=request.POST["reorder_level"]
)
        

        messages.success(request, "Product added successfully.")
        return redirect("view_products")

    return render(request, "products/add_product.html")


def view_products(request):
    products = Product.objects.all()
    return render(request, "products/view_products.html", {"products": products})


def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        product.product_id = request.POST["product_id"]
        product.product_name = request.POST["product_name"]
        product.price = request.POST["price"]
        product.quantity = request.POST["quantity"]
        product.save()

        return redirect("view_products")

    return render(request, "products/edit_product.html", {"product": product})

def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect("view_products")