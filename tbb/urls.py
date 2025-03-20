from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from pages import views as pages_views

urlpatterns = [
    path('', include('pages.urls')),
    # path('services', include('services.urls')),
    path('accounts/', include('accounts.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('chat/', include('chat.urls')),
    # path('contacts/', include('contacts.urls')),
    # path('projects', include('projects.urls')),
    path('admin/', admin.site.urls),
]

# Custom 404 error handler
# handler404 = pages_views.custom_404_view

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
