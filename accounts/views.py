from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic.edit import FormView
from .forms import UpdateUsernameForm

@method_decorator(login_required, name='dispatch')
class UpdateUsernameView(FormView):
    template_name = 'accounts/update_username.html'
    form_class = UpdateUsernameForm
    success_url = reverse_lazy('dashboard')  # Redirect to a relevant page after success

    def get_form(self, form_class=None):
        return self.form_class(instance=self.request.user)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your username has been updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error updating your username. Please try again.')
        return super().form_invalid(form)




    

