from django.contrib.admin import AdminSite
from django.contrib import admin
from django.apps import apps
from home.models import (
    HeroSection, AboutSection, ServiceCard, ServicesSection, 
    PricingPlan, PricingSection, ServiceOrder, PricingOrder, Contact
)

# Custom AdminSite class to control the admin dashboard appearance and behavior
class MyAdminSite(AdminSite):
    """
    Custom admin site for InvestNest, providing a tailored experience with
    a customized site header, title, and sorted model ordering.
    """
    site_header = 'InvestNest Admin'
    site_title = 'InvestNest Admin Portal'
    index_title = 'Welcome to InvestNest Admin Portal'

    def get_app_list(self, request):
        """
        Overrides the default app list to sort models in a specific order.
        """
        app_dict = self._build_app_dict(request)

        # Define the order in which the models should be displayed
        model_order = [
            'Hero sections', 'About sections', 'Service cards', 
            'Service orders', 'Services sections', 'Pricing plans', 
            'Pricing orders', 'Pricing sections', 'Contact'
        ]

        # Sort the models within each app by the defined order
        for app in app_dict.values():
            app['models'].sort(
                key=lambda x: model_order.index(x['name']) 
                if x['name'] in model_order else len(model_order)
            )

        # Sort the apps alphabetically and return
        return sorted(app_dict.values(), key=lambda x: x['name'].lower())


# Singleton ModelAdmin class for models with a single instance
class SingletonModelAdmin(admin.ModelAdmin):
    """
    This custom ModelAdmin prevents creating or deleting instances
    for singleton models. Only editing the existing instance is allowed.
    """

    def has_add_permission(self, request):
        # Prevent adding a new instance if one already exists
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the existing instance
        return False

    def has_change_permission(self, request, obj=None):
        """
        Allow editing only if an instance exists. If obj is None,
        it checks whether an instance already exists in the database.
        """
        if obj is None:
            return self.model.objects.exists()
        return True

    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        """
        Redirects to the edit page of the existing singleton instance.
        """
        # Load the existing instance and redirect to its change view
        obj = self.model.load()
        return super(SingletonModelAdmin, self).change_view(
            request, str(obj.pk), form_url, extra_context
        )


# Instantiate the custom admin site
admin_site = MyAdminSite(name='myadmin')


# Registering models for the custom admin site
admin_site.register(HeroSection, SingletonModelAdmin)
admin_site.register(AboutSection, SingletonModelAdmin)
admin_site.register(ServiceCard)
admin_site.register(ServiceOrder)
admin_site.register(ServicesSection, SingletonModelAdmin)
admin_site.register(PricingPlan)
admin_site.register(PricingOrder)
admin_site.register(PricingSection, SingletonModelAdmin)
admin_site.register(Contact)


# Registering models from other apps dynamically, except for models
# from the 'home' app, which are already manually registered.
for model in apps.get_models():
    if model._meta.app_label != 'home':
        try:
            admin_site.register(model)
        except admin.sites.AlreadyRegistered:
            # If the model is already registered, skip it
            pass
