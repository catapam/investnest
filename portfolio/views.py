import json
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import (
    JsonResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
    )
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
    )
from django.urls import reverse
from .models import Portfolio, Asset, Transaction
from .forms import PortfolioForm, AssetForm, TransactionForm
from .mixins import SafeDispatchMixin


# Redirects the user to the main portfolio view
def redirect_to_view(request):
    return redirect('portfolio')


# View to list all portfolios belonging to the logged-in user
@method_decorator(login_required, name='dispatch')
class PortfolioListView(SafeDispatchMixin, TemplateView):
    template_name = 'portfolio/portfolio_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portfolios = Portfolio.objects.filter(user=self.request.user)

        # Update portfolio stats for each portfolio before displaying
        for portfolio in portfolios:
            portfolio.update_portfolio_stats()

        context['portfolios'] = portfolios
        return context


# View to create a new portfolio
@method_decorator(login_required, name='dispatch')
class PortfolioCreateView(SafeDispatchMixin, CreateView):
    model = Portfolio
    form_class = PortfolioForm
    template_name = 'portfolio/portfolio_new.html'

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)

        # Set the user to the logged-in user
        form.instance.user = self.request.user
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Portfolio created successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('portfolio_detail', kwargs={'pk': self.object.pk})


# View to display the details of a specific portfolio
@method_decorator(login_required, name='dispatch')
class PortfolioDetailView(SafeDispatchMixin, TemplateView):
    template_name = 'portfolio/portfolio_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portfolio = get_object_or_404(
            Portfolio,
            pk=self.kwargs['pk'],
            user=self.request.user,
            )
        assets = portfolio.assets.all()

        # Calculate the total value of assets with valid transactions
        total_value_sum = sum(
            asset.get_total_value(
                ) for asset in assets if asset.transactions.exists())

        context['portfolio'] = portfolio
        context['assets'] = assets
        context['total_value_sum'] = total_value_sum
        portfolio.update_portfolio_stats()
        return context


# View to update a portfolio's details
@method_decorator(login_required, name='dispatch')
class PortfolioUpdateView(SafeDispatchMixin, UpdateView):
    def post(self, request, pk):
        portfolio = get_object_or_404(Portfolio, pk=pk)
        data = json.loads(request.body)

        # Update the portfolio's fields
        portfolio.name = data.get('name', portfolio.name)
        portfolio.description = data.get('description', portfolio.description)
        portfolio.color = data.get('color', portfolio.color)
        portfolio.save()
        portfolio.update_portfolio_stats()

        # Return a success message as JSON
        messages.success(self.request, 'Portfolio updated successfully!')
        return JsonResponse({'status': 'success'})

    def get(self, request, *args, **kwargs):
        messages.error(self.request, 'Something went wrong, try again!')
        return


# View to delete a portfolio
@method_decorator(login_required, name='dispatch')
class PortfolioDeleteView(SafeDispatchMixin, DeleteView):
    model = Portfolio
    template_name = 'portfolio/delete_confirm.html'

    def get_object(self, queryset=None):
        portfolio = super().get_object(queryset)
        if portfolio.user != self.request.user:
            messages.error(
                self.request,
                'You do not have permission to delete this portfolio.',
                )
            return None
        portfolio.update_portfolio_stats()
        return portfolio

    def post(self, request, *args, **kwargs):
        portfolio = self.get_object()
        if not portfolio:
            return HttpResponseForbidden(render(request, '401.html'))
        messages.success(self.request, 'Portfolio deleted successfully!')
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('portfolio')


# View to update an asset within a portfolio
@method_decorator(login_required, name='dispatch')
class AssetUpdateView(SafeDispatchMixin, UpdateView):
    model = Asset
    form_class = AssetForm
    template_name = 'portfolio/edit_asset.html'

    def get_queryset(self):
        portfolio = get_object_or_404(
            Portfolio,
            pk=self.kwargs['portfolio_pk'],
            user=self.request.user,
            )
        return portfolio.assets.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        asset = self.get_object()
        context['portfolio'] = asset.portfolio
        context['transactions'] = asset.transactions.all()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Asset updated successfully!')
        return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        messages.error(self.request, 'The asset update failed!')
        return self.render_to_response(self.get_context_data(form=form))


# View to delete an asset from a portfolio
@method_decorator(login_required, name='dispatch')
class AssetDeleteView(SafeDispatchMixin, DeleteView):
    model = Asset
    template_name = 'portfolio/delete_confirm.html'

    def get_object(self, queryset=None):
        asset = super().get_object(queryset)
        portfolio = get_object_or_404(
            Portfolio,
            pk=self.kwargs['portfolio_pk'],
            user=self.request.user,
        )
        if asset.portfolio != portfolio:
            messages.error(
                self.request,
                'You do not have permission to delete this asset.',
            )
            return None

        portfolio.update_portfolio_stats()
        return asset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolio'] = get_object_or_404(
            Portfolio,
            pk=self.kwargs['portfolio_pk'],
            user=self.request.user,
        )
        context['asset'] = get_object_or_404(Asset, pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        asset = self.get_object()
        if not asset:
            return HttpResponseForbidden(render(request, '401.html'))
        messages.success(self.request, 'Asset deleted successfully!')
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'portfolio_detail',
            kwargs={'pk': self.kwargs['portfolio_pk']},
            )


# View to create a new transaction for an asset
@method_decorator(login_required, name='dispatch')
class TransactionCreateView(SafeDispatchMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'portfolio/transaction_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        portfolio = get_object_or_404(
            Portfolio,
            pk=self.kwargs['portfolio_pk'],
            user=self.request.user,
            )
        kwargs['portfolio'] = portfolio

        # Set initial value for asset_choice
        initial_data = kwargs.get('initial', {})
        initial_data['asset_choice'] = '----'  # Default to "----" for asset

        asset_pk = self.kwargs.get('asset_pk')
        if asset_pk:
            asset = get_object_or_404(Asset, pk=asset_pk, portfolio=portfolio)

            # Update to asset.pk if present
            initial_data['asset_choice'] = asset.pk

            # Populate the name of the existing asset
            initial_data['new_asset_name'] = asset.name

        kwargs['initial'] = initial_data
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        portfolio = get_object_or_404(
            Portfolio,
            pk=self.kwargs['portfolio_pk'],
            user=self.request.user,
            )
        context['portfolio'] = portfolio

        asset_pk = self.kwargs.get('asset_pk')
        if asset_pk:
            context['asset'] = get_object_or_404(
                Asset, pk=asset_pk, portfolio=portfolio)

        context['referrer'] = self.request.META.get(
            'HTTP_REFERER',
            reverse('portfolio_detail',
                    kwargs={'pk': self.kwargs['portfolio_pk']},
                    ),
                        )
        return context

    def form_valid(self, form):
        portfolio = get_object_or_404(
            Portfolio,
            pk=self.kwargs['portfolio_pk'],
            user=self.request.user,
                )
        form.instance.portfolio = portfolio

        asset_choice = form.cleaned_data.get('asset_choice')
        new_asset_name = form.cleaned_data.get('new_asset_name')

        if 'asset_pk' in self.kwargs:
            asset = get_object_or_404(
                Asset,
                pk=self.kwargs['asset_pk'],
                portfolio=portfolio,
                    )
        elif asset_choice == 'new' and new_asset_name:
            asset, created = Asset.objects.get_or_create(
                name=new_asset_name,
                portfolio=portfolio,
                    )
            self.asset_pk = asset.pk  # Set asset_pk for the new asset
        else:
            asset = Asset.objects.get(pk=asset_choice)
            self.asset_pk = asset.pk  # Set asset_pk for the existing asset

        form.instance.asset = asset
        portfolio.update_portfolio_stats()
        messages.success(self.request, 'Transaction added successfully!')
        portfolio.update_portfolio_stats()
        return super().form_valid(form)

    def form_invalid(self, form):
        # If the form is invalid, re-render the page with errors
        messages.error(
            self.request,
            'There was an error in your submission.'
            ' Please correct the highlighted fields.',
                )
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse(
            'edit_asset',
            kwargs={
                'portfolio_pk': self.kwargs['portfolio_pk'],
                'pk': self.asset_pk
                },
                )


# View to update a transaction
@method_decorator(login_required, name='dispatch')
class UpdateTransactionView(SafeDispatchMixin, UpdateView):
    def post(self, request, portfolio_pk, asset_pk, transaction_id):
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        portfolio = get_object_or_404(Portfolio, pk=portfolio_pk)
        data = json.loads(request.body)

        # Update transaction fields
        transaction.type = data.get('type', transaction.type)
        transaction.action = data.get('action', transaction.action)
        transaction.quantity = data.get('quantity', transaction.quantity)
        transaction.price = data.get('price', transaction.price)
        transaction.date = data.get('date', transaction.date)
        transaction.save()
        portfolio.update_portfolio_stats()

        messages.success(self.request, 'Transaction updated successfully!')
        portfolio.update_portfolio_stats()
        return JsonResponse({'status': 'success'})

    def get(self, request, *args, **kwargs):
        messages.error(self.request, 'Something went wrong, try again!')
        return JsonResponse(
            {
                'status': 'error',
                'message': 'GET method is not allowed for this view.'
            },
            status=405,
                )


# View to delete a transaction
@method_decorator(login_required, name='dispatch')
class DeleteTransactionView(SafeDispatchMixin, DeleteView):
    model = Transaction
    template_name = 'portfolio/delete_confirm.html'

    def get_object(self, queryset=None):
        transaction = super().get_object(queryset)
        asset = get_object_or_404(Asset, pk=self.kwargs['asset_pk'])
        portfolio = get_object_or_404(
            Portfolio,
            pk=self.kwargs['portfolio_pk'],
            user=self.request.user,
                )
        if transaction.asset != asset:
            messages.error(
                self.request,
                'You do not have permission to delete this transaction.',
                    )
            return None

        portfolio.update_portfolio_stats()
        return transaction

    def post(self, request, *args, **kwargs):
        transaction = self.get_object()
        if not transaction:
            return HttpResponseForbidden(render(request, '401.html'))

        messages.success(self.request, 'Transaction deleted successfully!')
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
            'edit_asset',
            kwargs={
                'portfolio_pk': self.kwargs['portfolio_pk'],
                'pk': self.kwargs['asset_pk'],
            },
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolio'] = get_object_or_404(
            Portfolio,
            pk=self.kwargs['portfolio_pk'],
            user=self.request.user,
                )
        context['asset'] = get_object_or_404(Asset, pk=self.kwargs['asset_pk'])
        return context
