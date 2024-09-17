from django.urls import path
from .views import Index, Wireframes

# Define URL patterns for the home app
urlpatterns = [
    # The home page route, served by the Index class-based view
    path('', Index.as_view(), name='home'),

    # The wireframes page route, served by the Wireframes class-based view
    path('wireframes/', Wireframes.as_view(), name='wireframes')
]
