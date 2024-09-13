from django.urls import path
from .views import MetricsView,redirect_to_view

urlpatterns = [
    path('', redirect_to_view),
    path('view/', MetricsView.as_view(), name='metrics'),
    path('<int:pk>/', MetricsView.as_view(), name='metrics_portfolio'),
]
