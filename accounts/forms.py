from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # If role is agent, require admin approval (approved remains False)
            if self.cleaned_data['role'] == 'agent':
                Profile.objects.filter(user=user).update(role='agent', approved=False)
            else:
                Profile.objects.filter(user=user).update(role='trader', approved=True)
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'bio'] 