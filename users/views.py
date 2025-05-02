from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserChangeForm, BusinessProfileForm, ClientProfileForm


def profile_view(request):
    return render(request, 'users/profile.html')


def edit_profile(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        
        if request.user.user_type == 'business':
            profile_form = BusinessProfileForm(request.POST, request.FILES, instance=request.user.business_profile)
        else:
            profile_form = ClientProfileForm(request.POST, instance=request.user.client_profile)
            
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        
        if request.user.user_type == 'business':
            profile_form = BusinessProfileForm(instance=request.user.business_profile)
        else:
            profile_form = ClientProfileForm(instance=request.user.client_profile)
    
    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def favorites_view(request):
    favorites = request.user.favorites.all()
    return render(request, 'users/favorites.html', {'favorites': favorites})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully. You can now log in.')
            return redirect('account_login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('/')