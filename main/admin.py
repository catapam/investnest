from django.contrib.admin import AdminSite
from django.contrib import admin
from home.models import HeroSection, AboutSection, ServiceCard, ServicesSection, PricingPlan, PricingSection, ServiceOrder, PricingOrder

class MyAdminSite(AdminSite):
    site_header = 'InvestNest Admin'
    site_title = 'InvestNest Admin Portal'
    index_title = 'Welcome to InvestNest Admin Portal'

    def get_app_list(self, request):
        app_dict = self._build_app_dict(request)
        # Sort the app's models here in the desired order
        model_order = [
            'Hero sections', 
            'About sections', 
            'Service cards',
            'Service orders', 
            'Services sections', 
            'Pricing plans', 
            'Pricing orders',
            'Pricing sections'
        ]
        for app in app_dict.values():
            app['models'].sort(
                key=lambda x: model_order.index(x['name']) if x['name'] in model_order else len(model_order)
            )
        return sorted(app_dict.values(), key=lambda x: x['name'].lower())
   
class SingletonModelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the instance
        return False

    def has_change_permission(self, request, obj=None):
        # Allow changing only if an instance exists
        if obj is None:
            return self.model.objects.exists()
        return True

    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        # Redirect to the existing instance's change view
        obj = self.model.load()
        return super(SingletonModelAdmin, self).change_view(request, str(obj.pk), form_url, extra_context)
    
# Instantiate the custom admin site
admin_site = MyAdminSite(name='myadmin')
    
# Register the models here.
admin_site.register(HeroSection, SingletonModelAdmin)
admin_site.register(AboutSection, SingletonModelAdmin)
admin_site.register(ServiceCard)
admin_site.register(ServiceOrder)
admin_site.register(ServicesSection, SingletonModelAdmin)
admin_site.register(PricingPlan)
admin_site.register(PricingOrder)
admin_site.register(PricingSection, SingletonModelAdmin)

# Register other apps by using the default admin site registrations
# This will make sure allauth and any other installed apps are also included
from django.apps import apps

for model in apps.get_models():
    if model._meta.app_label != 'home':
        try:
            admin_site.register(model)
        except admin.sites.AlreadyRegistered:
            pass
