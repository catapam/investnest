from django.views.generic import TemplateView

# Create your views here.
class Portfolio(TemplateView):
    template_name = 'portfolio/portfolio.html'