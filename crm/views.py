from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Enquiry
from customers.models import Customer


def dashboard(request):

    enquiries = Enquiry.objects.all().order_by("-created_at")

    context = {
        "enquiries": enquiries,
        "total_enquiries": enquiries.count(),
        "new_enquiries": enquiries.filter(status="New").count(),
        "followups": enquiries.filter(status="Follow-up").count(),
        "quotations": enquiries.filter(status="Quotation").count(),
        "won": enquiries.filter(status="Won").count(),
    }

    return render(
        request,
        "crm/dashboard.html",
        context
    )


def new_enquiry(request):

    customers = Customer.objects.all().order_by(
        "customer_name"
    )

    if request.method == "POST":

        enquiry_no = request.POST.get("enquiry_no")
        customer_id = request.POST.get("customer")
        project_name = request.POST.get("project_name")

        if not enquiry_no:
            messages.error(
                request,
                "Enquiry number is required."
            )
            return redirect("crm_new_enquiry")

        if not customer_id:
            messages.error(
                request,
                "Please select a customer."
            )
            return redirect("crm_new_enquiry")

        if not project_name:
            messages.error(
                request,
                "Project name is required."
            )
            return redirect("crm_new_enquiry")

        if Enquiry.objects.filter(
            enquiry_no=enquiry_no
        ).exists():

            messages.error(
                request,
                "Enquiry number already exists."
            )
            return redirect("crm_new_enquiry")

        customer = get_object_or_404(
            Customer,
            id=customer_id
        )

        Enquiry.objects.create(

            enquiry_no=enquiry_no,

            customer=customer,

            company=request.POST.get(
                "company",
                ""
            ),

            contact_person=request.POST.get(
                "contact_person",
                ""
            ),

            phone=request.POST.get(
                "phone",
                ""
            ),

            email=request.POST.get(
                "email",
                ""
            ),

            city=request.POST.get(
                "city",
                ""
            ),

            project_name=project_name,

            sales_executive=request.POST.get(
                "sales_executive",
                ""
            ),

            expected_value=request.POST.get(
                "expected_value"
            ) or 0,

            expected_closing_date=request.POST.get(
                "expected_closing_date"
            ) or None,

            lead_source=request.POST.get(
                "lead_source",
                "Website"
            ),

            status=request.POST.get(
                "status",
                "New"
            ),

            notes=request.POST.get(
                "notes",
                ""
            ),

            drawing=request.FILES.get(
                "drawing"
            ),
        )

        messages.success(
            request,
            "Enquiry created successfully."
        )

        return redirect("crm_dashboard")

    return render(
        request,
        "crm/new_enquiry.html",
        {
            "customers": customers
        }
    )


def enquiry_details(request, id):

    enquiry = get_object_or_404(
        Enquiry,
        id=id
    )

    return render(
        request,
        "crm/enquiry_details.html",
        {
            "enquiry": enquiry
        }
    )


def edit_enquiry(request, id):

    enquiry = get_object_or_404(
        Enquiry,
        id=id
    )

    customers = Customer.objects.all().order_by(
        "customer_name"
    )

    if request.method == "POST":

        enquiry.customer_id = request.POST.get(
            "customer"
        )

        enquiry.company = request.POST.get(
            "company",
            ""
        )

        enquiry.contact_person = request.POST.get(
            "contact_person",
            ""
        )

        enquiry.phone = request.POST.get(
            "phone",
            ""
        )

        enquiry.email = request.POST.get(
            "email",
            ""
        )

        enquiry.city = request.POST.get(
            "city",
            ""
        )

        enquiry.project_name = request.POST.get(
            "project_name"
        )

        enquiry.sales_executive = request.POST.get(
            "sales_executive",
            ""
        )

        enquiry.expected_value = request.POST.get(
            "expected_value"
        ) or 0

        enquiry.expected_closing_date = request.POST.get(
            "expected_closing_date"
        ) or None

        enquiry.lead_source = request.POST.get(
            "lead_source",
            "Website"
        )

        enquiry.status = request.POST.get(
            "status",
            "New"
        )

        enquiry.notes = request.POST.get(
            "notes",
            ""
        )

        if request.FILES.get("drawing"):
            enquiry.drawing = request.FILES.get(
                "drawing"
            )

        enquiry.save()

        messages.success(
            request,
            "Enquiry updated successfully."
        )

        return redirect(
            "crm_enquiry_details",
            id=id
        )

    return render(
        request,
        "crm/edit_enquiry.html",
        {
            "enquiry": enquiry,
            "customers": customers
        }
    )