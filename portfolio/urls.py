from django.urls import path
from .views import (
    PortfolioListView,
    PortfolioCreateView,
    PortfolioDetailView,
    PortfolioDeleteView,
    AssetCreateView,
    AssetUpdateView,
    AssetDeleteView
)

urlpatterns = [
    path('', PortfolioListView.as_view(), name='portfolio'),
    path('new/', PortfolioCreateView.as_view(), name='portfolio_new'),
    path('<int:pk>/', PortfolioDetailView.as_view(), name='portfolio_detail'),
    path('<int:pk>/delete/', PortfolioDeleteView.as_view(), name='portfolio_delete'),

    # Asset management URLs
    path('<int:portfolio_pk>/asset/new/', AssetCreateView.as_view(), name='portfolio_add_asset'),
    path('<int:portfolio_pk>/asset/<int:pk>/edit/', AssetUpdateView.as_view(), name='portfolio_edit_asset'),
    path('<int:portfolio_pk>/asset/<int:pk>/delete/', AssetDeleteView.as_view(), name='portfolio_delete_asset'),
]
