from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser


def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        middle_name = request.POST.get('middle_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        role = request.POST.get('role', '0')

        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return render(request, 'authentication/register.html')

        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/register.html')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists.')
            return render(request, 'authentication/register.html')

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            role=int(role),
            is_active=True,
        )
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('book_list')

    return render(request, 'authentication/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.email}!')
            return redirect('book_list')
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'authentication/login.html')

    return render(request, 'authentication/login.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out.')
    return redirect('login')


def user_list_view(request):
    users = CustomUser.get_all()
    return render(request, 'authentication/user_list.html', {'users': users})


def user_detail_view(request, user_id):
    user_obj = get_object_or_404(CustomUser, id=user_id)
    return render(request, 'authentication/user_detail.html', {'user_obj': user_obj})
