from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=255, blank=True) 
    image = CloudinaryField('image', blank=True, folder="TradeByBarter")
    preferred_trades = models.CharField(max_length=255, blank=True) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class TradeRequest(models.Model):
    id = models.CharField(max_length=24, primary_key=True)  # Change ID to CharField
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    sender = models.ForeignKey(User, related_name='trade_requests_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='trade_requests_received', on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    image = CloudinaryField('image', blank=True, folder="TradeByBarter")
    message = models.TextField(blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Request from {self.sender} to {self.receiver} for {self.listing.title}"