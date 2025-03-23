# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, ProfileForm 
from .models import Profile 
from .decorators import agent_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from utils import get_db_handle
from bson import ObjectId
import hashlib

# MongoDB connection parameters
from pymongo import MongoClient
client = MongoClient('mongodb+srv://sarah:Puffalump123@cluster0.6kmuw7y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['Cluster0']

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user using Django's User model
            user.email = form.cleaned_data['email']
            user.role = form.cleaned_data['role']
            # Hash the password before saving
            hashed_password = hashlib.sha256(form.cleaned_data['password1'].encode()).hexdigest()
            user_data = {
                'username': user.username,
                'email': user.email,
                'password': hashed_password,
                'role': user.role
            }
            db.users.insert_one(user_data)  # Save user data to MongoDB
            
            role = form.cleaned_data.get('role')
            if role == 'agent':
                approved = False 
            else:
                approved = True 

            user.save()  # Save the user first
            Profile.objects.create(user=user, role=role, approved=approved)  # Create the profile after saving the user

            login(request, user)  # Log the user in
            return redirect('index')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user against MongoDB
        user_data = db.users.find_one({'username': username})
        if user_data and user_data['password'] == hashlib.sha256(password.encode()).hexdigest():
            user = authenticate(request, username=username, password=password)  # Authenticate against Django's User model
            login(request, user)  # Log the user in
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
