from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .utils import send_registration_email
from django.utils.html import strip_tags

# Create your views here.
def login_user(request):
    if request.method != 'POST':
        return render(request,'user/login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        user = CustomUser.objects.get(username=username)
    except CustomUser.DoesNotExist:
        messages.error(request,'username does not exist')
        return render(request,'user/login.html')
    user = authenticate(request, username=username, password=password)

    if user is None:
        messages.error(request,'Incorrect password')
        return render(request, 'user/login.html')
    elif user.is_active:
        login(request,user)
        messages.success(request,'Logged in successfully')
    else:
        messages.error(request,'Please activate your account or contact admin')
        return render(request,'user/login.html')
    return redirect('home')

def user_registration(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            
            user = form.save()

            login(request, user)
            return redirect('home')
        else:
            error = strip_tags(form.errors)
            messages.error(request, f"Error : {error}")
    return render(request, 'user/register.html')

def logout_user(request):
    if request.method != 'POST':
        return render(request,'user/logout.html')
    logout(request)
    messages.success(request,'Logged out successfully!')
    return redirect('home')