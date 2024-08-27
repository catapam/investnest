from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseForbidden
from django.urls import reverse
from .models import Portfolio, Asset, Transaction
from .forms import PortfolioForm, AssetForm, TransactionForm

@method_decorator(login_required, name='dispatch')
class PortfolioListView(TemplateView):
    template_name = 'portfolio/portfolio_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolios'] = Portfolio.objects.filter(user=self.request.user)
        return context

@method_decorator(login_required, name='dispatch')
class PortfolioCreateView(CreateView):
    model = Portfolio
    form_class = PortfolioForm
    template_name = 'portfolio/portfolio_new.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Portfolio created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('portfolio')  

@method_decorator(login_required, name='dispatch')
class PortfolioDetailView(TemplateView):
    template_name = 'portfolio/portfolio_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portfolio = get_object_or_404(Portfolio, pk=self.kwargs['pk'], user=self.request.user)
        assets = portfolio.assets.all()

        # Sum only the assets that have a valid total value
        total_value_sum = sum(asset.get_total_value() for asset in assets if asset.transactions.exists())

        context['portfolio'] = portfolio
        context['assets'] = assets
        context['total_value_sum'] = total_value_sum
        return context

@method_decorator(login_required, name='dispatch')
class PortfolioDeleteView(DeleteView):
    model = Portfolio
    template_name = 'portfolio/portfolio_confirm_delete.html'

    def get_object(self, queryset=None):
        portfolio = super().get_object(queryset)
        if portfolio.user != self.request.user:
            messages.error(self.request, 'You do not have permission to delete this portfolio.')
            return None 
        return portfolio

    def delete(self, request, *args, **kwargs):
        portfolio = self.get_object()
        if not portfolio:
            return HttpResponseForbidden(render(request, '401.html')) 
        messages.success(request, 'Portfolio deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('portfolio')  


@method_decorator(login_required, name='dispatch')
class AssetCreateView(CreateView):
    model = Asset
    form_class = AssetForm
    template_name = 'portfolio/portfolio_add_asset.html'

    def form_valid(self, form):
        portfolio = get_object_or_404(Portfolio, pk=self.kwargs['portfolio_pk'], user=self.request.user)
        form.instance.portfolio = portfolio
        messages.success(self.request, 'Asset added successfully!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolio'] = get_object_or_404(Portfolio, pk=self.kwargs['portfolio_pk'], user=self.request.user)
        return context

    def get_success_url(self):
        return reverse('portfolio_detail', kwargs={'pk': self.kwargs['portfolio_pk']})

@method_decorator(login_required, name='dispatch')
class AssetUpdateView(UpdateView):
    model = Asset
    form_class = AssetForm  # Update this form to exclude price and quantity
    template_name = 'portfolio/portfolio_edit_asset.html'

    def get_queryset(self):
        portfolio = get_object_or_404(Portfolio, pk=self.kwargs['portfolio_pk'], user=self.request.user)
        return portfolio.assets.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asset = self.get_object()
        context['portfolio'] = asset.portfolio
        context['transactions'] = asset.transactions.all()
        return context

    def get_success_url(self):
        return reverse('portfolio_detail', kwargs={'pk': self.kwargs['portfolio_pk']})

@method_decorator(login_required, name='dispatch')
class AssetDeleteView(DeleteView):
    model = Asset
    template_name = 'portfolio/portfolio_delete_asset.html'

    def get_queryset(self):
        portfolio = get_object_or_404(Portfolio, pk=self.kwargs['portfolio_pk'], user=self.request.user)
        return portfolio.assets.all()

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Asset deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('portfolio_detail', kwargs={'pk': self.kwargs['portfolio_pk']})

@method_decorator(login_required, name='dispatch')
class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'portfolio/transaction_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        portfolio = get_object_or_404(Portfolio, pk=self.kwargs['portfolio_pk'], user=self.request.user)
        kwargs['portfolio'] = portfolio

        if 'asset_pk' in self.kwargs:
            asset = get_object_or_404(Asset, pk=self.kwargs['asset_pk'], portfolio=portfolio)
            kwargs['initial'] = {'asset': asset.pk}  # Pass the asset's primary key

        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portfolio = get_object_or_404(Portfolio, pk=self.kwargs['portfolio_pk'], user=self.request.user)
        context['portfolio'] = portfolio

        if 'asset_pk' in self.kwargs:
            context['asset'] = get_object_or_404(Asset, pk=self.kwargs['asset_pk'], portfolio=portfolio)

        # Pass the referrer to the template
        context['referrer'] = self.request.META.get('HTTP_REFERER', reverse('portfolio_detail', kwargs={'pk': self.kwargs['portfolio_pk']}))

        return context

    def form_valid(self, form):
        portfolio = get_object_or_404(Portfolio, pk=self.kwargs['portfolio_pk'], user=self.request.user)
        form.instance.portfolio = portfolio

        asset_choice = form.cleaned_data.get('asset_choice')
        new_asset_name = form.cleaned_data.get('new_asset_name')

        if asset_choice == 'new' and new_asset_name:
            asset, created = Asset.objects.get_or_create(
                name=new_asset_name,
                portfolio=portfolio
            )
        else:
            asset = Asset.objects.get(pk=asset_choice)

        form.instance.asset = asset
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('portfolio_detail', kwargs={'pk': self.kwargs['portfolio_pk']})

