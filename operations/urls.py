from django.urls import path
from .views import OperationsView

urlpatterns = [
    path('', OperationsView.as_view(), name='operations'),
]
