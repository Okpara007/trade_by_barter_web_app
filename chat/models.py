from django.db import models
from django.contrib.auth.models import User
from marketplace.models import Listing  

class ChatRoom(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    participants = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat for {self.listing.title}"

class ChatMessage(models.Model):
    chat_room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.message[:20]}"
