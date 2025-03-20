# marketplace/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.listings, name='listings'),
    path('create/', views.create_listing, name='create_listing'),
    path('<int:pk>/', views.listing, name='listing'),
    path('requests/create/<int:listing_id>/', views.trade_request_create, name='trade_request_create'),
    path('requests/', views.trade_request_list, name='trade_request_list'),
    path('requests/<int:pk>/', views.trade_request_detail, name='trade_request_detail'),
    path('requests/<int:pk>/accept/', views.trade_request_accept, name='trade_request_accept'),
    path('requests/<int:pk>/reject/', views.trade_request_reject, name='trade_request_reject'),
    path('search/', views.listing_search, name='listing_search'),
]
