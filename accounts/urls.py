from django.urls import path
from .views import UpdateUsernameView, redirect_to_user

urlpatterns = [
    path('', redirect_to_user),
    path('user/', UpdateUsernameView.as_view(), name='account_user'),
]
