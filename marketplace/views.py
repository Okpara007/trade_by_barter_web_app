# marketplace/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Listing, TradeRequest
from .forms import ListingForm, TradeRequestForm

def listings(request):
    """
    Display a list of all listings.
    """
    listings = Listing.objects.all().order_by('-created_at')
    return render(request, 'marketplace/listings.html', {'listings': listings})

@login_required
def create_listing(request):
    """
    Allow a logged-in user to create a new listing.
    """
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.created_by = request.user  # Associate the listing with the logged-in user
            listing.save()
            return redirect('listing', pk=listing.pk)
    else:
        form = ListingForm()
    return render(request, 'marketplace/create_listing.html', {'form': form})

def listing(request, pk):
    """
    Show detailed information for a single listing identified by its primary key.
    """
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'marketplace/listing.html', {'listing': listing})

@login_required
def trade_request_create(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == 'POST':
        form = TradeRequestForm(request.POST)
        if form.is_valid():
            trade_request = form.save(commit=False)
            trade_request.sender = request.user
            trade_request.receiver = listing.created_by
            trade_request.listing = listing
            trade_request.save()
            messages.success(request, "Trade request sent successfully!")
            return redirect('listing', pk=listing.pk)
    else:
        form = TradeRequestForm()

    return render(request, 'marketplace/trade_request_create.html', {
        'form': form,
        'listing': listing,
    })

@login_required
def trade_request_list(request):
    # Show trade requests where the user is either sender or receiver
    sent_requests = TradeRequest.objects.filter(sender=request.user)
    received_requests = TradeRequest.objects.filter(receiver=request.user)
    return render(request, 'marketplace/trade_request_list.html', {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    })

@login_required
def trade_request_detail(request, pk):
    trade_request = get_object_or_404(TradeRequest, pk=pk)

    # Check if the current user has permission to view or manage this request
    if trade_request.receiver != request.user and trade_request.sender != request.user:
        messages.error(request, "You do not have permission to view this trade request.")
        return redirect('trade_request_list')

    return render(request, 'marketplace/trade_request_detail.html', {
        'trade_request': trade_request,
    })

@login_required
def trade_request_accept(request, pk):
    trade_request = get_object_or_404(TradeRequest, pk=pk)
    if trade_request.receiver == request.user and trade_request.status == 'pending':
        trade_request.status = 'accepted'
        trade_request.save()
        messages.success(request, "Trade request accepted.")
    else:
        messages.error(request, "You cannot accept this request.")
    return redirect('trade_request_detail', pk=pk)

@login_required
def trade_request_reject(request, pk):
    trade_request = get_object_or_404(TradeRequest, pk=pk)
    if trade_request.receiver == request.user and trade_request.status == 'pending':
        trade_request.status = 'rejected'
        trade_request.save()
        messages.success(request, "Trade request rejected.")
    else:
        messages.error(request, "You cannot reject this request.")
    return redirect('trade_request_detail', pk=pk)
