from django.urls import path
from .views import MetricsView,RedirectMetricsView

# Define URL patterns for the metrics application
urlpatterns = [
    # Redirect root URL ('') to the main metrics view
    path('', RedirectMetricsView.as_view()),

    # Main metrics page view
    path('view/', MetricsView.as_view(), name='metrics'),

    # Portfolio specific metrics
    path('<int:pk>/', MetricsView.as_view(), name='metrics_portfolio'),
]
