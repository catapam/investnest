import logging
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

# Initialize the logger
logger = logging.getLogger(__name__)


class SafeDispatchMixin:
    """
    Mixin that overrides the dispatch method to safely handle exceptions during
    request processing. It logs any exceptions encountered and displays
    an error message to the user, redirecting them to a safe fallback page.
    """
    def dispatch(self, request, *args, **kwargs):
        """
        Override the default dispatch method to include exception handling.

        Args:
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: The response from the parent dispatch method,
            or a redirect in case of an error.
        """
        try:
            # Call the parent dispatch method (which will handle the request)
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            # Log the error details
            logger.error(f"Error in {self.__class__.__name__}: {str(e)}")

            # Add an error message to be shown to the user
            messages.error(
                self.request,
                'An error occurred! Please try again or contact support.'
            )

            # Redirect to a safe page, typically the portfolio detail page
            return HttpResponseRedirect(
                reverse(
                    'portfolio_detail',
                    kwargs={'pk': self.kwargs.get('portfolio_pk')}))
