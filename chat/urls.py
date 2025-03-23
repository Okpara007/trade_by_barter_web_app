from django.urls import path
from . import views  

urlpatterns = [
    path('my-chats/', views.my_chats, name='my_chats'),
    path('<int:listing_id>/', views.chat_view, name='chat_view'),
]
