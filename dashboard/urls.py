from django.urls import path
from .views import DashboardView,RedirectDashboardView

# Define URL patterns for the dashboard application
urlpatterns = [
    # Redirect root URL ('') to the main dashboard view
    path('', RedirectDashboardView.as_view()),

    # Main dashboard page view
    path('view/', DashboardView.as_view(), name='dashboard'),
]
