from django.urls import path
from .views import OperationsView,redirect_to_view

urlpatterns = [
    path('', redirect_to_view),
    path('view/', OperationsView.as_view(), name='operations'),
]
