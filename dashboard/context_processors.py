from portfolio.models import Portfolio 

def intra_menu_processor(request):
    intra_menu = []
    current_path = request.path

    if current_path.startswith('/accounts'):
        intra_menu = [
            {'name': 'User', 'url': '/accounts/', 'icon': 'fa-regular fa-user'},
            {'name': 'Email', 'url': '/accounts/email/', 'icon': 'fa-regular fa-envelope'},
            {'name': 'Password', 'url': '/accounts/password/change/', 'icon': 'fa-solid fa-key'},
        ]
    elif current_path.startswith('/dashboard'):
        intra_menu = [
            {'name': 'Main', 'url': '/dashboard/', 'icon': 'fas fa-home'},
        ]
        
    elif current_path.startswith('/portfolio'):
        portfolios = Portfolio.objects.filter(user=request.user)
        intra_menu = [
            {'name': 'View', 'url': '/portfolio/', 'icon': 'fa-solid fa-eye'},
            {'name': 'New', 'url': '/portfolio/new/', 'icon': 'fa-solid fa-plus'},
            ]
        for portfolio in portfolios:
            intra_menu.append({
            'name': portfolio.name,
            'url': f'/portfolio/{portfolio.pk}/',
            'icon': 'fa-solid fa-briefcase',
            'color': portfolio.color 
        })
            
    elif current_path.startswith('/contact'):
        intra_menu = [
            {'name': 'View', 'url': '/contact/view/', 'icon': 'fa-solid fa-eye'},
        ]
    elif current_path.startswith('/metrics'):
        intra_menu = [
            {'name': 'View', 'url': '/metrics/view/', 'icon': 'fa-solid fa-eye'},
        ]
    elif current_path.startswith('/operations'):
        intra_menu = [
            {'name': 'View', 'url': '/operations/view/', 'icon': 'fa-solid fa-eye'},
        ]

    return {'intra_menu': intra_menu}