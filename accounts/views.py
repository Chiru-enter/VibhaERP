from django.shortcuts import render, redirect
from django.db.models import Sum, F
from django.db.models.functions import ExtractMonth

from products.models import Product
from customers.models import Customer
from suppliers.models import Supplier
from sales.models import Sale
from purchase.models import Purchase


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "admin" and password == "1234":
            return redirect("dashboard")
        else:
            return render(
                request,
                "accounts/login.html",
                {"error": "Invalid Username or Password"},
            )

    return render(request, "accounts/login.html")


def dashboard(request):

    # -------------------------------
    # Dashboard Cards
    # -------------------------------

    total_products = Product.objects.count()
    total_customers = Customer.objects.count()
    total_suppliers = Supplier.objects.count()
    total_sales = Sale.objects.count()
    total_purchases = Purchase.objects.count()

    # -------------------------------
    # Inventory Value
    # -------------------------------

    inventory_value = 0

    for product in Product.objects.all():
        inventory_value += product.price * product.quantity

    # -------------------------------
    # Outstanding Amounts
    # -------------------------------

    receivables = (
        Sale.objects.aggregate(
            total=Sum("balance_amount")
        )["total"]
        or 0
    )

    payables = (
        Purchase.objects.aggregate(
            total=Sum("balance_amount")
        )["total"]
        or 0
    )

    # -------------------------------
    # Recent Transactions
    # -------------------------------

    recent_sales = Sale.objects.order_by("-sale_date")[:5]

    recent_purchases = Purchase.objects.order_by("-purchase_date")[:5]

    # -------------------------------
    # Low Stock Products
    # -------------------------------

    low_stock = Product.objects.filter(quantity__lte=10)

    # -------------------------------
    # Monthly Sales Chart
    # -------------------------------

    sales_chart = (
        Sale.objects
        .annotate(month=ExtractMonth("sale_date"))
        .values("month")
        .annotate(total=Sum("grand_total"))
        .order_by("month")
    )

    sales_labels = []
    sales_values = []

    month_names = [
        "",
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]

    for row in sales_chart:
        sales_labels.append(month_names[row["month"]])
        sales_values.append(float(row["total"]))

    # -------------------------------
    # Monthly Purchase Chart
    # -------------------------------

    purchase_chart = (
        Purchase.objects
        .annotate(month=ExtractMonth("purchase_date"))
        .values("month")
        .annotate(total=Sum("grand_total"))
        .order_by("month")
    )

    purchase_labels = []
    purchase_values = []

    for row in purchase_chart:
        purchase_labels.append(month_names[row["month"]])
        purchase_values.append(float(row["total"]))

    context = {

        "total_products": total_products,
        "total_customers": total_customers,
        "total_suppliers": total_suppliers,
        "total_sales": total_sales,
        "total_purchases": total_purchases,

        "inventory_value": inventory_value,
        "receivables": receivables,
        "payables": payables,

        "recent_sales": recent_sales,
        "recent_purchases": recent_purchases,

        "low_stock": low_stock,

        "sales_labels": sales_labels,
        "sales_values": sales_values,

        "purchase_labels": purchase_labels,
        "purchase_values": purchase_values,
    }

    return render(
        request,
        "accounts/dashboard.html",
        context,
    )