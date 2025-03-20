# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, ProfileForm 
from .models import Profile 
from .decorators import agent_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            
            role = form.cleaned_data.get('role')
            if role == 'agent':
                approved = False 
            else:
                approved = True 

            Profile.objects.create(user=user, role=role, approved=approved)

            login(request, user)
            return redirect('index')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('index')

@agent_required
def agent_dashboard(request):
    return render(request, 'accounts/agent_dashboard.html')

@login_required
def profile_view(request):
    profile = request.user.profile  

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()  
            return redirect('profile') 
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'form': form
    })