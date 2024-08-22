from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UpdateUsernameForm

@login_required
def update_username(request):
    if request.method == 'POST':
        form = UpdateUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your username has been updated successfully!')
            return redirect('dashboard')  # Redirect to a relevant page after success
        else:
            messages.error(request, 'There was an error updating your username. Please try again.')
    else:
        form = UpdateUsernameForm(instance=request.user)
    
    return render(request, 'accounts/update_username.html', {'form': form})
