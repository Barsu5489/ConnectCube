from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from users.models import Company, Customer, User

from .models import Service, ServiceHistory, ServiceRequest
from .forms import CreateNewService, RequestServiceForm

from django.db.models import Count

def service_list(request):
    services = Service.objects.all().order_by("-date")
    service_counts = (
    ServiceRequest.objects
    .values('service__id', 'service__name')
    .annotate(request_count=Count('id'))
    .order_by('-request_count')
    )
    return render(request, "services/list.html", {"services": services, "service_counts": service_counts })

def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, "services/single_service.html", {"service": service})


def create(request):
    # CHANGED: Get company and use its available fields
    try:
        company = Company.objects.get(user=request.user)
        choices = company.get_available_service_fields()  # ← NEW: Dynamic choices
    except Company.DoesNotExist:
        from users.models import SERVICE_FIELD_CHOICES
        choices = SERVICE_FIELD_CHOICES
    
    if request.method == "POST":
        form = CreateNewService(request.POST, choices=choices)
        if form.is_valid():
            Service.objects.create(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                price_hour=form.cleaned_data["price_hour"],
                field=form.cleaned_data["field"],
                company=company,  # ← CHANGED: Use the company variable
            )
            return redirect("services_list")
    else:
        form = CreateNewService(choices=choices)
    
    return render(request, "services/create.html", {"form": form})



def service_field(request, field):
    # search for the service present in the url
    field = field.replace("-", " ").title()
    
    # Get services that match the field OR are from "All in One" companies
    from django.db.models import Q
    services = Service.objects.filter(
        Q(field=field) |  
        Q(company__field="All in One")  
    )
    
    return render(
        request, "services/field.html", {"services": services, "field": field}
    )

def request_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)

    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            request_date = form.cleaned_data['request_date']
            notes = form.cleaned_data['notes']
            duration_hours = form.cleaned_data['duration_hours']
            address = form.cleaned_data['address']

            # Get the customer instance
            customer = Customer.objects.get(user=request.user)

            # Calculate total price
            price_per_hour = service.price_hour  
            total_price = duration_hours * price_per_hour

            # Save to DB
            ServiceRequest.objects.create(
                service=service,
                customer=customer,
                request_date=request_date,
                notes=notes,
                duration_hours=duration_hours,
                address=address,
                total_price=total_price
            )

            return redirect('services_list')
    else:
        form = RequestServiceForm()

    return render(request, 'services/request_service.html', {
        'form': form,
        'service': service
    })

