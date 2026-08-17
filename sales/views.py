from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from decimal import Decimal

from customers.models import Customer
from products.models import Product
from inventory.models import Inventory

from .models import Sale, SaleItem, SalePayment


def dashboard(request):
    return render(request, "sales/dashboard.html")


def new_sale(request):
    customers = Customer.objects.all()
    products = Product.objects.all()

    if request.method == "POST":
        invoice_no = request.POST["invoice_no"]
        customer = Customer.objects.get(id=request.POST["customer"])
        product = Product.objects.get(id=request.POST["product"])
        quantity = int(request.POST["quantity"])
        paid_amount = Decimal(request.POST["paid_amount"])

        inventory = Inventory.objects.get(product=product)

        if quantity > inventory.quantity:
            messages.error(request, "Not enough stock available.")
            return render(
                request,
                "sales/new_sale.html",
                {
                    "customers": customers,
                    "products": products,
                },
            )

        sub_total = product.price * quantity

        sale = Sale(
            invoice_no=invoice_no,
            customer=customer,
            sub_total=sub_total,
            paid_amount=paid_amount,
        )

        sale.calculate_totals()
        sale.save()

        SaleItem.objects.create(
            sale=sale,
            product=product,
            quantity=quantity,
            price=product.price,
            total=sub_total,
        )

        inventory.quantity -= quantity
        inventory.save()

        messages.success(request, "Sale created successfully.")
        return redirect("sales_history")

    return render(
        request,
        "sales/new_sale.html",
        {
            "customers": customers,
            "products": products,
        },
    )


def sales_history(request):
    sales = Sale.objects.all().order_by("-sale_date", "-id")

    return render(
        request,
        "sales/sales_history.html",
        {
            "sales": sales,
        },
    )


def invoice_details(request, id):
    sale = get_object_or_404(Sale, id=id)

    items = SaleItem.objects.filter(sale=sale)

    payments = SalePayment.objects.filter(
        sale=sale
    ).order_by("-payment_date")

    return render(
        request,
        "sales/invoice_details.html",
        {
            "sale": sale,
            "items": items,
            "payments": payments,
        },
    )


def add_item(request, id):
    sale = get_object_or_404(Sale, id=id)

    products = Product.objects.all()

    if request.method == "POST":

        product = Product.objects.get(id=request.POST["product"])
        quantity = int(request.POST["quantity"])

        inventory = Inventory.objects.get(product=product)

        if quantity > inventory.quantity:
            messages.error(request, "Not enough stock available.")
            return redirect("add_item", id=id)

        line_total = product.price * quantity

        SaleItem.objects.create(
            sale=sale,
            product=product,
            quantity=quantity,
            price=product.price,
            total=line_total,
        )

        inventory.quantity -= quantity
        inventory.save()

        sale.sub_total += line_total
        sale.calculate_totals()
        sale.save()

        messages.success(request, "Item added successfully.")

        return redirect("invoice_details", id=id)

    return render(
        request,
        "sales/add_item.html",
        {
            "sale": sale,
            "products": products,
        },
    )


def receive_payment(request, id):

    sale = get_object_or_404(Sale, id=id)

    if request.method == "POST":

        amount = Decimal(request.POST["amount"])

        payment_mode = request.POST["payment_mode"]

        remarks = request.POST.get("remarks", "")

        if amount <= Decimal("0.00"):
            messages.error(
                request,
                "Payment amount must be greater than zero."
            )
            return redirect("receive_payment", id=id)

        if amount > sale.balance_amount:
            messages.error(
                request,
                "Payment amount cannot be greater than the balance amount."
            )
            return redirect("receive_payment", id=id)

        SalePayment.objects.create(
            sale=sale,
            amount=amount,
            payment_mode=payment_mode,
            remarks=remarks,
        )

        sale.paid_amount += amount

        sale.calculate_totals()

        sale.save()

        messages.success(
            request,
            "Payment received successfully."
        )

        return redirect("invoice_details", id=id)

    payments = SalePayment.objects.filter(
        sale=sale
    ).order_by("-payment_date")

    return render(
        request,
        "sales/receive_payment.html",
        {
            "sale": sale,
            "payments": payments,
        },
    )