from django.views.generic import TemplateView


# Class-based view for handling 401 Unauthorized error
class Custom401View(TemplateView):
    """
    This view renders a custom 401 error page when the user is unauthorized.
    It uses the '401.html' template and returns an HTTP status code of 401.
    """
    template_name = '401.html'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and returns the 401 status with the
        custom template.
        """
        response = super().get(request, *args, **kwargs)
        response.status_code = 401
        return response


# Class-based view for handling 404 Not Found error
class Custom404View(TemplateView):
    """
    This view renders a custom 404 error page when the page is not found.
    It uses the '404.html' template and returns an HTTP status code of 404.
    """
    template_name = '404.html'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and returns the 404 status with the
        custom template.
        """
        response = super().get(request, *args, **kwargs)
        response.status_code = 404
        return response
