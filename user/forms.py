from django import forms 
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','email','password1','password2','phone_number','first_name','last_name' )