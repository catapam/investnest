from django.views.generic import TemplateView


class Index(TemplateView):
    template_name= 'home/index.html'

class Wireframes(TemplateView):
    template_name= 'home/wireframes.html'