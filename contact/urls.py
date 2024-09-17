from django.urls import path
from .views import ContactView, RedirectContactView

# Define URL patterns for the contact application
urlpatterns = [
    # Redirect root URL ('') to the main contact view
    path('', RedirectContactView.as_view()),  

    # Main contact page view
    path('view/', ContactView.as_view(), name='contact'),
]
