from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserDetail 
from .models import Donation


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['first_name','last_name','phone_number','gender','address','pincode','city','state','country']
        exclude = ('user',)

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['category', 'description', 'quantity', 'image']