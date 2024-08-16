from django.urls import path
from .views import Index, Wireframes

urlpatterns=[
    path('', Index.as_view(), name='home'),
    path('wireframes/', Wireframes.as_view(), name='wireframes')
]