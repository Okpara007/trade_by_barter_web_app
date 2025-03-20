from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = (
        ('trader', 'Trader'),
        ('agent', 'Agent'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    # Agents require admin approval; traders are automatically approved
    approved = models.BooleanField(default=True)
    bio = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f"{self.user.username} - {self.role}"
