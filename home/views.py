from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .models import (
    HeroSection,
    AboutSection,
    ServicesSection,
    PricingSection,
    ServiceOrder,
    PricingOrder,
    Contact
)
from .forms import ContactForm


# Class-based view for the Home page (Index)
class Index(TemplateView):
    # Specify the template to use for the home page
    template_name = 'home/index.html'

    # Define the context data passed to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Load the Hero and About sections (Singleton models)
        context['hero_section'] = HeroSection.load()
        context['about_section'] = AboutSection.load()

        # Retrieve and order services linked to the ServicesSection
        context['services_section'] = ServicesSection.load()
        ordered_services = ServiceOrder.objects.filter(
            service_section=context['services_section']
        ).order_by('order')
        context['ordered_services'] = [
            service_order.service for service_order in ordered_services
        ]

        # Retrieve and order pricing linked to the PricingSection
        context['pricing_section'] = PricingSection.load()
        ordered_pricing = PricingOrder.objects.filter(
            pricing_section=context['pricing_section']
        ).order_by('order')
        context['ordered_pricing'] = [
            pricing_order.pricing for pricing_order in ordered_pricing
        ]

        # Add the contact form to the context
        context['contact_form'] = ContactForm()

        # Check if the form was successfully submitted
        context['form_submitted'] = self.request.GET.get('submitted', False)

        return context

    # Handle form submission via POST request
    def post(self, request, *args, **kwargs):
        # Instantiate the contact form with POST data
        contact_form = ContactForm(request.POST, request=request)

        # Check if the form is valid
        if contact_form.is_valid():
            # Save the valid form
            contact_form.save()
            # Redirect to prevent duplicate submissions
            return redirect(f'{self.request.path}?submitted=True')

        # If the form is invalid, re-render the page with errors
        context = self.get_context_data()
        # Return form with validation errors
        context['contact_form'] = contact_form
        # Flag to indicate a form error occurred
        context['form_error'] = True
        return self.render_to_response(context)


# Class-based view for the Wireframes page
class Wireframes(TemplateView):
    # Specify the template to use for the wireframes page
    template_name = 'home/wireframes.html'
