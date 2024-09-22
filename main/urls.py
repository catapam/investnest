from django.contrib import admin
from django.urls import path, include
from .admin import admin_site
from .views import Custom401View, Custom404View

# URL patterns for the project
urlpatterns = [
    # Custom admin site URL
    path("admin/", admin_site.urls),

    # Home app URLs
    path('', include('home.urls')),

    # Dashboard app URLs
    path('dashboard/', include('dashboard.urls')),

    # Portfolio app URLs
    path('portfolio/', include('portfolio.urls')),

    # Authentication and account management URLs from 'allauth' and custom app
    path('accounts/', include('allauth.urls')),  # Third-party auth package
    path('accounts/', include('accounts.urls')),  # Custom account-related URLs

    # Operations app URLs
    path('operations/', include('operations.urls')),

    # Contact app URLs
    path('contact/', include('contact.urls')),

    # Metrics app URLs
    path('metrics/', include('metrics.urls')),

    # Custom error pages for 401 Unauthorized and 404 Not Found
    path('401/', Custom401View.as_view(), name='custom_401'),
    path('404/', Custom404View.as_view(), name='custom_404'),
]
