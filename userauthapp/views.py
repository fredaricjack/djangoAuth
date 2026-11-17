
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .forms import UserForm

User = get_user_model()


# REGISTER
def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = UserForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.email = form.cleaned_data['email'].strip()
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.success(
                request,
                'Account created successfully! Please login.'
            )

            return redirect('login')

    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form})


# READ
@login_required(login_url='login')
def read(request):

    return render(request, 'read.html', {
        'user': request.user
    })


# UPDATE
@login_required(login_url='login')
def update(request):

    user = request.user

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        if not username or not email:
            messages.error(request, 'Username and email are required.')

        elif User.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.error(request, 'Username already exists.')

        elif User.objects.filter(email=email).exclude(pk=user.pk).exists():
            messages.error(request, 'Email already exists.')

        else:
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name

            user.save()

            messages.success(request, 'Account updated successfully!')

            return redirect('home')

    return render(request, 'update.html', {'user': user})


# DELETE
@login_required(login_url='login')
@require_POST
def delete(request):

    user = request.user

    logout(request)
    user.delete()

    messages.success(request, 'Your account has been deleted successfully!')

    return redirect('login')


# LOGIN
def user_login(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                'Login successful!'
            )

            return redirect('home')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(request, 'login.html')


# HOME
@login_required(login_url='login')
def home(request):

    return render(request, 'home.html')


# LOGOUT
@require_POST
@login_required(login_url='login')
def user_logout(request):

    logout(request)

    messages.success(
        request,
        'You have logged out successfully.'
    )

    return redirect('login')
