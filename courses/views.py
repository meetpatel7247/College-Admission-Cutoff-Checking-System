from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import College, Course, UserProfile
from django.contrib.auth.decorators import login_required

def home(request):
    colleges = College.objects.all()
    return render(request, 'home.html', {'colleges': colleges})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        percentage = request.POST.get('percentage')

        # Check password match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
            return render(request, 'signup.html')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'signup.html')

        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create profile linked with percentage
        UserProfile.objects.create(user=user, percentage=percentage)

        # Auto login after signup
        login(request, user)
        messages.success(request, "Signup successful! Welcome.")
        return redirect('home')

    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def search_view(request):
    if request.method == 'POST':
        stream = request.POST.get('stream')
        percentage = request.POST.get('percentage')

        try:
            percentage = float(percentage)
            if percentage > 100 or percentage < 0:
                messages.error(request, 'Percentage must be between 0 and 100.')
                return render(request, 'search.html')
        except ValueError:
            messages.error(request, 'Invalid percentage value.')
            return render(request, 'search.html')

        courses = Course.objects.filter(stream=stream, min_percentage__lte=percentage)
        return render(request, 'search.html', {'courses': courses})
    return render(request, 'search.html')