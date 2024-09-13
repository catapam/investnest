from django.urls import path
from .views import (
    PortfolioListView,
    PortfolioCreateView,
    PortfolioDetailView,
    PortfolioUpdateView,
    PortfolioDeleteView,
    AssetUpdateView,
    AssetDeleteView,
    TransactionCreateView,
    UpdateTransactionView,
    DeleteTransactionView,
    redirect_to_view
)

urlpatterns = [
    path('', redirect_to_view),
    path('view/', PortfolioListView.as_view(), name='portfolio'),
    path('new/', PortfolioCreateView.as_view(), name='portfolio_new'),
    path('<int:pk>/', PortfolioDetailView.as_view(), name='portfolio_detail'),
    path('<int:pk>/edit/', PortfolioUpdateView.as_view(), name='portfolio_edit'),
    path('<int:pk>/delete/', PortfolioDeleteView.as_view(), name='portfolio_delete'),

    path('<int:portfolio_pk>/asset/new/', TransactionCreateView.as_view(), name='portfolio_add_asset'),
    path('<int:portfolio_pk>/asset/<int:pk>/edit/', AssetUpdateView.as_view(), name='portfolio_edit_asset'),
    path('<int:portfolio_pk>/asset/<int:pk>/delete/', AssetDeleteView.as_view(), name='portfolio_delete_asset'),

    path('<int:portfolio_pk>/asset/<int:asset_pk>/transaction/add/', TransactionCreateView.as_view(), name='transaction_add'),
    path('<int:portfolio_pk>/asset/<int:asset_pk>/transaction/<int:transaction_id>/update/', UpdateTransactionView.as_view(), name='update_transaction'),
    path('<int:portfolio_pk>/asset/<int:asset_pk>/transaction/<int:pk>/delete/', DeleteTransactionView.as_view(), name='delete_transaction'),
]

