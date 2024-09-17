from django.urls import path
from .views import UpdateUsernameView, RedirectUserView

# Define the URL patterns for the 'accounts' app
urlpatterns = [
    # Root URL redirects to the user update page
    path('', RedirectUserView.as_view()),  # Redirects to the user's profile or update page

    # URL for updating the user's username
    path('user/', UpdateUsernameView.as_view(), name='account_user'),
]
