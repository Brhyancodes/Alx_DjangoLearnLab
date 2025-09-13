from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("relationship_app.urls")),
    # Add other app URLs here if you have them
    path("bookshelf/", include("bookshelf.urls")),  # If you have bookshelf app
]

# Add media URL configuration for development
# This allows Django to serve uploaded files (like profile photos) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
