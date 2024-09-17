from django.urls import path
from .views import OperationsView,RedirectOperationsView

# Define URL patterns for the operations application
urlpatterns = [
    # Redirect root URL ('') to the main operations view
    path('', RedirectOperationsView.as_view()),

    # Main operations page view
    path('view/', OperationsView.as_view(), name='operations'),
]
