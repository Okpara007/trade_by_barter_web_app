from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Listing, TradeRequest
import cloudinary
import cloudinary.uploader
from bson import ObjectId  # Import ObjectId for MongoDB
from django.utils import timezone
from .forms import ListingForm, TradeRequestForm, ListingSearchForm
from django.db.models import Q
from django.contrib.auth.models import User

# MongoDB connection parameters
from pymongo import MongoClient
client = MongoClient('mongodb+srv://sarah:Puffalump123@cluster0.6kmuw7y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['Cluster0']

def listings(request):
    """
    Display a list of all listings.
    """
    listings_data = db.listings.find().sort('created_at', -1)  # Fetch listings from MongoDB
    listings = [{'title': listing['title'], 'description': listing['description'], 'created_at': listing['created_at'], 'preferred_trades': listing['preferred_trades'], 'image': listing['image'], 'id': listing['_id']} for listing in listings_data]  # Convert to list of dictionaries
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
            listing.created_by = request.user  
            # Upload the image to Cloudinary
            upload_result = cloudinary.uploader.upload(form.cleaned_data['image'])
            image_url = upload_result['secure_url']
            
            # Save the listing to MongoDB with the image URL
            listing_data = {
                'title': listing.title,
                'description': listing.description,
                'created_at': timezone.now(),
                'created_by': request.user,
                'category': form.cleaned_data['category'],
                'location': form.cleaned_data['location'],
                'preferred_trades': form.cleaned_data['preferred_trades'],
                'image': image_url
            }
            result = db.listings.insert_one(listing_data)  # Insert listing into MongoDB
            return redirect('listing', pk=str(result.inserted_id))  # Redirect using MongoDB's _id
    else:
        form = ListingForm()
    return render(request, 'marketplace/create_listing.html', {'form': form})

def listing(request, pk):
    listing_data = db.listings.find_one({'_id': ObjectId(pk)})  # Fetch listing from MongoDB
    if listing_data is None:
        raise Http404("Listing not found")
    listing_obj = {
        'title': listing_data['title'],
        'description': listing_data['description'],
        'created_at': listing_data['created_at'],
        'created_by': listing_data['created_by'],
        'location': listing_data['location'],
        'preferred_trades': listing_data['preferred_trades'],
        'image': listing_data['image'],
        'pk': str(listing_data['_id'])  # Add the pk attribute
    }
    is_owner = request.user.is_authenticated and (request.user.username == listing_obj['created_by'])
    return render(request, 'marketplace/listing.html', {
        'listing': listing_obj,
        'is_owner': is_owner
    })

@login_required
def trade_request_create(request, pk):
    listing_data = db.listings.find_one({'_id': ObjectId(pk)})
    if request.method == 'POST':
        form = TradeRequestForm(request.POST)
        if form.is_valid():
            trade_request = form.save(commit=False)
            trade_request.sender = request.user
            trade_request.receiver = User.objects.get(username=listing_data['created_by'])
            
            # Create a new Listing instance using the MongoDB data
            new_listing = Listing.objects.create(
                title=listing_data['title'],
                description=listing_data['description'],
                created_at=timezone.now(),
                created_by=request.user,
                category=listing_data['category'],
                location=listing_data['location'],
                preferred_trades=listing_data['preferred_trades'],
                image=listing_data['image']
            )
            trade_request.listing = new_listing
            
            trade_request.save()
            messages.success(request, "Trade request sent successfully!")
            return redirect('listing', pk=pk)
    else:
        form = TradeRequestForm()

    return render(request, 'marketplace/trade_request_create.html', {
        'form': form,
        'listing': listing,
    })

@login_required
def trade_request_list(request):
    sent_requests = TradeRequest.objects.filter(sender=request.user)
    received_requests = TradeRequest.objects.filter(receiver=request.user)
    return render(request, 'marketplace/trade_request_list.html', {
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    })

@login_required
def trade_request_detail(request, pk):
    trade_request = get_object_or_404(TradeRequest, pk=pk)

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

def listing_search(request):
    form = ListingSearchForm(request.GET or None)
    listings_data = db.listings.find().sort('created_at', -1)  # Fetch listings from MongoDB
    listings = [{'title': listing['title'], 'description': listing['description'], 'created_at': listing['created_at'], 'location': listing['location'], 'preferred_trades': listing['preferred_trades'], 'image': listing['image'], 'id': listing['_id']} for listing in listings_data]  # Convert to list of dictionaries

    if form.is_valid():
        category = form.cleaned_data.get('category')
        location = form.cleaned_data.get('location')
        query = form.cleaned_data.get('query')
        listings = listings.filter(location__icontains=location)
        if query:
            listings = listings.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

    context = {
        'form': form,
        'listings': listings,
    }
