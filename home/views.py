from django.views.generic import TemplateView
from django.shortcuts import render
from .models import HeroSection, AboutSection, ServicesSection, PricingSection, ServiceOrder, PricingOrder

class Index(TemplateView):
    template_name= 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hero_section'] = HeroSection.load()
        context['about_section'] = AboutSection.load()

        # Get ordered services
        context['services_section'] = ServicesSection.load()
        ordered_services = ServiceOrder.objects.filter(service_section=context['services_section']).order_by('order')
        context['ordered_services'] = [service_order.service for service_order in ordered_services]

        # Get ordered pricing
        context['pricing_section'] = PricingSection.load()
        ordered_pricing = PricingOrder.objects.filter(pricing_section=context['pricing_section']).order_by('order')
        context['ordered_pricing'] = [pricing_order.pricing for pricing_order in ordered_pricing]

        return context

class Wireframes(TemplateView):
    template_name= 'home/wireframes.html'