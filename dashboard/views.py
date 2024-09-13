from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import redirect

def redirect_to_main(request):
    return redirect('dashboard')

@method_decorator(login_required, name='dispatch')
class Dashboard(TemplateView):
    template_name = 'dashboard/dashboard.html'