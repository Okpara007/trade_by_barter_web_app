from django.urls import path
from . import views

urlpatterns = [
    path('listing/<int:listing_id>/', views.chat_view, name='chat_view'),
]
