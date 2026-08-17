from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas

from sales.models import Sale
from purchase.models import Purchase
from inventory.models import Inventory


def dashboard(request):
    return render(request, "reports/dashboard.html")


def sales_report(request):
    sales = Sale.objects.all().order_by("-sale_date")
    return render(
        request,
        "reports/sales_report.html",
        {"sales": sales},
    )


def purchase_report(request):
    purchases = Purchase.objects.all().order_by("-purchase_date")
    return render(
        request,
        "reports/purchase_report.html",
        {"purchases": purchases},
    )


def inventory_report(request):
    inventory = Inventory.objects.all()
    return render(
        request,
        "reports/inventory_report.html",
        {"inventory": inventory},
    )


def sales_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="sales_report.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 20)
    p.drawString(180, 800, "Vibha ERP")

    p.setFont("Helvetica-Bold", 16)
    p.drawString(170, 775, "Sales Report")

    y = 730

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Invoice")
    p.drawString(170, y, "Customer")
    p.drawString(330, y, "Date")
    p.drawString(450, y, "Total")

    y -= 20

    sales = Sale.objects.all().order_by("-sale_date")
    total = 0

    p.setFont("Helvetica", 12)

    for sale in sales:
        p.drawString(50, y, sale.invoice_no)
        p.drawString(170, y, sale.customer.customer_name)
        p.drawString(330, y, str(sale.sale_date))
        p.drawString(450, y, str(sale.total_amount))

        total += sale.total_amount
        y -= 20

        if y < 50:
            p.showPage()
            y = 800

    p.setFont("Helvetica-Bold", 13)
    p.drawString(320, y - 20, "Grand Total:")
    p.drawString(450, y - 20, str(total))

    p.save()
    return response
def purchase_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="purchase_report.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 20)
    p.drawString(180, 800, "Vibha ERP")

    p.setFont("Helvetica-Bold", 16)
    p.drawString(160, 775, "Purchase Report")

    y = 730

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Invoice")
    p.drawString(170, y, "Supplier")
    p.drawString(330, y, "Date")
    p.drawString(450, y, "Total")

    y -= 20

    purchases = Purchase.objects.all().order_by("-purchase_date")
    total = 0

    p.setFont("Helvetica", 12)

    for purchase in purchases:
        p.drawString(50, y, purchase.purchase_no)
        p.drawString(170, y, purchase.supplier.supplier_name)
        p.drawString(330, y, str(purchase.purchase_date))
        p.drawString(450, y, str(purchase.total_amount))

        total += purchase.total_amount
        y -= 20

        if y < 50:
            p.showPage()
            y = 800
            p.setFont("Helvetica", 12)

    p.setFont("Helvetica-Bold", 13)
    p.drawString(320, y - 20, "Grand Total:")
    p.drawString(450, y - 20, str(total))

    p.save()
    return response

def inventory_pdf(request):
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="inventory_report.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 20)
    p.drawString(180, 800, "Vibha ERP")

    p.setFont("Helvetica-Bold", 16)
    p.drawString(165, 775, "Inventory Report")

    y = 730

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Product")
    p.drawString(220, y, "Stock")
    p.drawString(330, y, "Reorder Level")
    p.drawString(470, y, "Status")

    y -= 20

    inventory = Inventory.objects.all()

    p.setFont("Helvetica", 12)

    for item in inventory:
        p.drawString(50, y, item.product.product_name)
        p.drawString(220, y, str(item.quantity))
        p.drawString(330, y, str(item.reorder_level))

        status = "Low" if item.quantity <= item.reorder_level else "Available"
        p.drawString(470, y, status)

        y -= 20

        if y < 50:
            p.showPage()
            y = 800
            p.setFont("Helvetica", 12)

    p.save()
    return response