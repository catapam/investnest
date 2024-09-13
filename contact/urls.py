from django.urls import path
from .views import ContactView, redirect_to_view

urlpatterns = [
    path('', redirect_to_view), 
    path('view/', ContactView.as_view(), name='contact'),
]
