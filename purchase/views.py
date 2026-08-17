from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from suppliers.models import Supplier
from products.models import Product
from inventory.models import Inventory

from .models import Purchase, PurchaseItem, PurchasePayment


def dashboard(request):
    return render(request, "purchase/dashboard.html")


def new_purchase(request):

    suppliers = Supplier.objects.all()

    if request.method == "POST":

        purchase_no = request.POST["purchase_no"]
        supplier = Supplier.objects.get(id=request.POST["supplier"])

        purchase = Purchase(
            purchase_no=purchase_no,
            supplier=supplier,
            sub_total=Decimal("0.00"),
            paid_amount=Decimal("0.00"),
        )

        purchase.calculate_totals()
        purchase.save()

        messages.success(request, "Purchase created successfully.")

        return redirect("purchase_details", id=purchase.id)

    return render(
        request,
        "purchase/new_purchase.html",
        {
            "suppliers": suppliers,
        },
    )


def purchase_history(request):

    purchases = Purchase.objects.all().order_by(
        "-purchase_date",
        "-id"
    )

    return render(
        request,
        "purchase/purchase_history.html",
        {
            "purchases": purchases,
        },
    )


def purchase_details(request, id):

    purchase = get_object_or_404(Purchase, id=id)

    items = PurchaseItem.objects.filter(
        purchase=purchase
    )

    payments = PurchasePayment.objects.filter(
        purchase=purchase
    ).order_by("-payment_date")

    return render(
        request,
        "purchase/purchase_details.html",
        {
            "purchase": purchase,
            "items": items,
            "payments": payments,
        },
    )


def add_item(request, id):

    purchase = get_object_or_404(Purchase, id=id)

    products = Product.objects.all()

    if request.method == "POST":

        product = Product.objects.get(
            id=request.POST["product"]
        )

        quantity = int(request.POST["quantity"])

        inventory = Inventory.objects.get(
            product=product
        )

        line_total = product.price * quantity

        PurchaseItem.objects.create(
            purchase=purchase,
            product=product,
            quantity=quantity,
            price=product.price,
            total=line_total,
        )

        inventory.quantity += quantity
        inventory.save()

        purchase.sub_total += line_total

        purchase.calculate_totals()

        purchase.save()

        messages.success(
            request,
            "Product added successfully."
        )

        return redirect(
            "purchase_details",
            id=id
        )

    return render(
        request,
        "purchase/add_item.html",
        {
            "purchase": purchase,
            "products": products,
        },
    )


def make_payment(request, id):

    purchase = get_object_or_404(
        Purchase,
        id=id
    )

    if request.method == "POST":

        amount = Decimal(
            request.POST["amount"]
        )

        payment_mode = request.POST[
            "payment_mode"
        ]

        remarks = request.POST.get(
            "remarks",
            ""
        )

        if amount <= Decimal("0.00"):

            messages.error(
                request,
                "Payment amount must be greater than zero."
            )

            return redirect(
                "make_payment",
                id=id
            )

        if amount > purchase.balance_amount:

            messages.error(
                request,
                "Payment amount cannot be greater than the balance amount."
            )

            return redirect(
                "make_payment",
                id=id
            )

        PurchasePayment.objects.create(
            purchase=purchase,
            amount=amount,
            payment_mode=payment_mode,
            remarks=remarks,
        )

        purchase.paid_amount += amount

        purchase.calculate_totals()

        purchase.save()

        messages.success(
            request,
            "Supplier payment recorded successfully."
        )

        return redirect(
            "purchase_details",
            id=id
        )

    payments = PurchasePayment.objects.filter(
        purchase=purchase
    ).order_by("-payment_date")

    return render(
        request,
        "purchase/make_payment.html",
        {
            "purchase": purchase,
            "payments": payments,
        },
    )