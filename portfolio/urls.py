from django.urls import path
from .views import (
    PortfolioListView,
    PortfolioCreateView,
    PortfolioDetailView,
    PortfolioDeleteView,
    AssetCreateView,
    AssetUpdateView,
    AssetDeleteView,
    TransactionCreateView,
    UpdateTransactionView,
    DeleteTransactionView
)

urlpatterns = [
    path('', PortfolioListView.as_view(), name='portfolio'),
    path('new/', PortfolioCreateView.as_view(), name='portfolio_new'),
    path('<int:pk>/', PortfolioDetailView.as_view(), name='portfolio_detail'),
    path('<int:pk>/delete/', PortfolioDeleteView.as_view(), name='portfolio_delete'),

    path('<int:portfolio_pk>/asset/new/', AssetCreateView.as_view(), name='portfolio_add_asset'),
    path('<int:portfolio_pk>/asset/<int:pk>/edit/', AssetUpdateView.as_view(), name='portfolio_edit_asset'),
    path('<int:portfolio_pk>/asset/<int:pk>/delete/', AssetDeleteView.as_view(), name='portfolio_delete_asset'),

    path('<int:portfolio_pk>/asset/<int:asset_pk>/transaction/add/', TransactionCreateView.as_view(), name='transaction_add'),
    path('transaction/update/<int:transaction_id>/', UpdateTransactionView.as_view(), name='update_transaction'),
    path('transaction/delete/<int:transaction_id>/', DeleteTransactionView.as_view(), name='delete_transaction'),
]

