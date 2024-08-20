from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .models import HeroSection, AboutSection, ServicesSection, PricingSection, ServiceOrder, PricingOrder, Contact
from .forms import ContactForm

class Index(TemplateView):
    template_name = 'home/index.html'

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

        # Include the contact form
        context['contact_form'] = ContactForm()

        # Check for success flag
        context['form_submitted'] = self.request.GET.get('submitted', False)

        return context

    def post(self, request, *args, **kwargs):
        # Handle the form submission
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect(f'{self.request.path}?submitted=True')  # Redirect to avoid re-submission and show the popup
        else:
            # Re-render the page with the form and errors
            context = self.get_context_data()
            context['contact_form'] = contact_form
            context['form_error'] = True  # Indicate that there was an error with the form submission
            return self.render_to_response(context)

class Wireframes(TemplateView):
    template_name= 'home/wireframes.html'