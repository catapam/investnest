from django.urls import path
from .views import Dashboard, redirect_to_main

urlpatterns=[
    path('', redirect_to_main), 
    path('main/', Dashboard.as_view(), name='dashboard'),
]