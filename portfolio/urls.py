from django.urls import path
from .views import Portfolio

urlpatterns=[
    path('', Portfolio.as_view(), name='portfolio')
]