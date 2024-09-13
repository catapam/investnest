from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import redirect

def redirect_to_view(request):
    return redirect('metrics')

@method_decorator(login_required, name='dispatch')
class MetricsView(TemplateView):
    template_name = 'metrics/metrics.html'