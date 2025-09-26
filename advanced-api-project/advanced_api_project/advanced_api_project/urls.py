"""
URL configuration for advanced_api_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # API Endpoints
    # All API routes will be prefixed with 'api/'
    # Access: http://localhost:8000/api/
    path("api/", include("api.urls")),
    # Django REST Framework Browsable API Authentication
    # Provides login/logout functionality for the browsable API
    # Access: http://localhost:8000/api-auth/
    path("api-auth/", include("rest_framework.urls")),
]

"""
=== MAIN URL CONFIGURATION ===

This configuration sets up three main URL patterns:

1. /admin/ - Django administration interface
   - Manage users, groups, and application data
   - Requires superuser account

2. /api/ - All API endpoints
   - Includes all URLs defined in api/urls.py
   - Prefixes all API routes with 'api/'

3. /api-auth/ - DRF authentication pages
   - Login/logout pages for the browsable API
   - Useful for testing and development

=== COMPLETE ENDPOINT STRUCTURE ===

After including api.urls, your complete API structure will be:

Book Management:
- GET    /api/books/                 -> BookListView
- GET    /api/books/<id>/            -> BookDetailView  
- POST   /api/books/create/          -> BookCreateView
- PUT    /api/books/<id>/update/     -> BookUpdateView
- PATCH  /api/books/<id>/update/     -> BookUpdateView
- DELETE /api/books/<id>/delete/     -> BookDeleteView

Author Management:
- GET    /api/authors/               -> AuthorListView
- GET    /api/authors/<id>/          -> AuthorDetailView

Authentication:
- GET    /api-auth/login/            -> Login page
- POST   /api-auth/logout/           -> Logout

Administration:
- GET    /admin/                     -> Django admin

=== DEVELOPMENT NOTES ===

1. The browsable API will be available at each endpoint when accessed via browser
2. Authentication pages are useful for manual testing
3. Make sure to run migrations before testing: python manage.py migrate
4. Create a superuser for admin access: python manage.py createsuperuser
"""
