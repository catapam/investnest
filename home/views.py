from django.views.generic import TemplateView
from django.shortcuts import render
from .models import HeroSection, AboutSection, ServicesSection, PricingSection

class Index(TemplateView):
    template_name= 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero_section'] = HeroSection.load()
        context['about_section'] = AboutSection.load()
        context['services_section'] = ServicesSection.load()
        context['pricing_section'] = PricingSection.load()
        return context

class Wireframes(TemplateView):
    template_name= 'home/wireframes.html'