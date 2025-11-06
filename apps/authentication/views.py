from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser


@csrf_protect
def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after registration
            login(request, user)
            messages.success(request, f'Welcome {user.username}! Your account has been created.')
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()

    return render(request, 'authentication/register.html', {'form': form})


@csrf_protect
def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')

                # Redirect to next parameter or dashboard
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'authentication/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard_view(request):
    """Dashboard view - only accessible to logged-in users"""
    return render(request, 'authentication/dashboard.html', {
        'user': request.user
    })


@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'authentication/profile.html', {
        'user': request.user
    })

def home_view(request):
    """Home page view"""
    return render(request, 'authentication/home.html')