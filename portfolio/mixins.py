import logging
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

logger = logging.getLogger(__name__)

class SafeDispatchMixin:
    """
    Mixin that overrides the dispatch method to handle exceptions and log them.
    """
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {self.__class__.__name__}: {str(e)}")
            messages.error(self.request, 'An error occurred! Please try again or contact support.')
            return HttpResponseRedirect(reverse('portfolio_detail', kwargs={'pk': self.kwargs.get('portfolio_pk')}))
