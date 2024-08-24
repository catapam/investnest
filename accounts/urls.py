from django.urls import path
from .views import UpdateUsernameView

urlpatterns = [
    path('', UpdateUsernameView.as_view(), name='account_user'),
]
