from django.contrib import admin
from django.urls import path, include
from .admin import admin_site
from .views import custom_401_view, custom_404_view

urlpatterns = [
    path("admin/", admin_site.urls),
    path('', include('home.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('portfolio/', include('portfolio.urls')),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('accounts.urls')), 
    path('operations/', include('operations.urls')),
    path('contact/', include('contact.urls')),
    path('metrics/', include('metrics.urls')),
    path('401/', custom_401_view, name='custom_401'),
    path('404/', custom_404_view, name='custom_404'),
]
