from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import redirect

def redirect_to_view(request):
    return redirect('contact')

@method_decorator(login_required, name='dispatch')
class ContactView(TemplateView):
    template_name = 'contact/contact.html'