from django.contrib import admin
from .models import Listing, TradeRequest

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description', 'created_by__username')

@admin.register(TradeRequest)
class TradeRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'listing', 'status', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'listing__title')
    list_filter = ('status', 'created_at')