from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm,UserDetailsForm,DonationForm
from django.shortcuts import render, redirect
from .models import Donation,UserDetail
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum,Count
from itertools import groupby



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('user_details')  # Redirect to home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_details(request):
    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            user_details = form.save(commit=False)
            user_details.user = request.user
            user_details.save()
            return redirect('donate')  # Redirect to success page
    else:
        form = UserDetailsForm()
    return render(request, 'user_details.html', {'form': form})


@login_required
def donate(request):
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            # Fetch the user details of the current user
            user_details = UserDetail.objects.get(user=request.user)
            donation.user_details = user_details  # Associate the user details with the donation
            donation.created_by = request.user
            donation.save()
            return redirect('donate_success')  # Redirect to success page
    else:
        form = DonationForm()
    return render(request, 'donate.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def donation_statistics(request):
    # Retrieve donation data
    category_city_totals = Donation.objects.values('category', 'user_details__city').annotate(total_quantity=Sum('quantity')).order_by('user_details__city', 'category')

    # Group donation data by city
    grouped_data = {}
    for city, data in groupby(category_city_totals, key=lambda x: x['user_details__city']):
        grouped_data[city] = list(data)

    context = {
        'grouped_data': grouped_data,
    }
    return render(request, 'donation_statistics.html', context)

    
@login_required
def donate_success(request):
    # Get the total number of items donated by the current user
    total_donations = Donation.objects.filter(created_by=request.user).count()

    # Customize your greeting message here
    greeting = "Thank you for your generous donation!"

    context = {
        'total_donations': total_donations,
        'greeting': greeting,
    }
    return render(request, 'donate_success.html', context)


def index(request):
    return render(request,'index.html')