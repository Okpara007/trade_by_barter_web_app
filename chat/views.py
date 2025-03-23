from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from marketplace.models import Listing
from .models import ChatRoom, ChatMessage

@login_required
def chat_view(request, listing_id):
    """
    Shows a chat interface for the given listing. 
    Both the listing owner and any buyer can see and send messages.
    """
    listing = get_object_or_404(Listing, pk=listing_id)

    chat_room, created = ChatRoom.objects.get_or_create(listing=listing)

    if listing.created_by not in chat_room.participants.all():
        chat_room.participants.add(listing.created_by)
    if request.user not in chat_room.participants.all():
        chat_room.participants.add(request.user)

    if request.method == "POST":
        message_text = request.POST.get('message')
        if message_text:
            ChatMessage.objects.create(
                chat_room=chat_room,
                sender=request.user,
                message=message_text
            )
        return redirect('chat_view', listing_id=listing_id)

    messages = chat_room.messages.order_by('timestamp')

    context = {
        'listing': listing,
        'chat_room': chat_room,
        'messages': messages,
    }
    return render(request, 'chat/chat_interface.html', context)


@login_required
def my_chats(request):
    """
    Lists all ChatRooms where the current user is a participant.
    """
    chat_rooms = ChatRoom.objects.filter(participants=request.user).distinct()
    return render(request, 'chat/chats.html', {'chat_rooms': chat_rooms})
