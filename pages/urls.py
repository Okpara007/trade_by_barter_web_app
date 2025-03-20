from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    # path('what_we_do', views.what_we_do, name='what_we_do'),
]

# if settings.DEBUG:  
#     urlpatterns += [
#         path('test-500/', views.test_500, name='test_500'),
#     ]