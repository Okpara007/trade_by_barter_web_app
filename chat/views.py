from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from marketplace.models import Listing

@login_required
def chat_view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    other_user = listing.created_by
    context = {
        'other_user_id': other_user.id,
        'other_user_name': other_user.username,
        'other_user_email': other_user.email,
    }
    return render(request, 'chat/chat_interface.html', context)
