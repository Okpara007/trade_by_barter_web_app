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
            # Create the user instance without immediately saving to database
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            
            # Retrieve the role from the form and set approval accordingly.
            role = form.cleaned_data.get('role')
            if role == 'agent':
                approved = False  # Agents require admin approval.
            else:
                approved = True   # Traders are automatically approved.
            
            # Create the Profile directly in the view.
            Profile.objects.create(user=user, role=role, approved=approved)
            
            # Automatically log in the user.
            login(request, user)
            return redirect('index')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        # Get username and password from POST data
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Log the user in
            login(request, user)
            return redirect('index')  # Replace 'index' with your preferred post-login page name
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    
    # For GET requests, just render the login form
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('index')

@agent_required
def agent_dashboard(request):
    # Your agent-specific logic here.
    return render(request, 'accounts/agent_dashboard.html')

@login_required
def profile_view(request):
    profile = request.user.profile  # Get the logged-in user's profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()  # Updates the profile in the database
            return redirect('profile')  # Refresh or redirect to a success page
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'form': form
    })