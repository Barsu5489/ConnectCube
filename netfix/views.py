from django.shortcuts import get_object_or_404, render

from users.models import User, Company, Customer
from services.models import Service, ServiceRequest


def home(request):
    return render(request, "users/home.html", {"user": request.user})



def customer_profile(request, name):
    # Get the Customer object by username of related User
    customer = get_object_or_404(Customer, user__username=name)

    # Filter ServiceHistory by the customer, NOT by user
    sh = ServiceRequest.objects.filter(customer=customer).order_by('-request_date')
    print(sh)
    return render(request, 'users/customer_profile.html', {
        'customer': customer,
        'sh':sh,
    })




def company_profile(request, name):
    # fetches the company user and all of the services available by it
    user = User.objects.get(username=name)
    services = Service.objects.filter(company=Company.objects.get(user=user)).order_by(
        "-date"
    )

    return render(request, "users/profile.html", {"user": user, "services": services})
