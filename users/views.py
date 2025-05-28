from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView, TemplateView

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User, Company, Customer
from django.contrib import messages


def register(request):
    return render(request, "users/register.html")


class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = "users/register_customer.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "customer"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("/")


class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = "users/register_company.html"

    def get_context_data(self, **kwargs):
        kwargs["user_type"] = "company"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect("/")


def LoginUserView(request):
    form = UserLoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email_or_username = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = User.objects.filter(email=email_or_username).first() or \
               User.objects.filter(username=email_or_username).first()

        if user:
            user = authenticate(request, username=user.username, password=password)
            if user:
                login(request, user)
                return redirect('/')
        form.add_error(None, "Invalid login credentials.")
    
    return render(request, 'users/login.html', {'form': form})