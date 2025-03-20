from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
]

# if settings.DEBUG:  
#     urlpatterns += [
#         path('test-500/', views.test_500, name='test_500'),
#     ]