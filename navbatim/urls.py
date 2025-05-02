from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('services/', include('services.urls')),
    path('appointments/', include('appointments.urls')),
    path('business/', include('business.urls')),  # Added business URLs
    path('accounts/', include('users.sign_urls')),  # Added business URLs
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
