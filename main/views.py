from django.shortcuts import render

def custom_401_view(request, exception=None):
    return render(request, '401.html', status=401)

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)