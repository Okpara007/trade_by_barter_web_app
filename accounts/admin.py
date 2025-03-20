# accounts/admin.py
from django.contrib import admin
from .models import Profile  # Import your Profile model

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'approved')
    # You can customize this as needed.
