from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from marketplace.models import Listing
from django.contrib import messages

@login_required
def chat_view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    
    # Prevent the listing owner from chatting with themselves
    if request.user == listing.created_by:
        messages.error(request, "You cannot chat with yourself.")
        return redirect('listing', pk=listing.pk)
    
    # Set the other user to the listing owner
    other_user = listing.created_by
    
    context = {
        'listing': listing,
        'other_user': other_user,
        'talkjs_app_id': 'tw6C1KHF',  # Your confirmed test app ID
    }
    return render(request, 'chat/chat_interface.html', context)