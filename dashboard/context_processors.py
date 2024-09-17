from portfolio.models import Portfolio

def intra_menu_processor(request):
    """
    Context processor to generate an intra-page menu based on the current URL path.
    The menu will be tailored to the specific section of the application the user is in.
    This is used for rendering intra-navigation menus dynamically across different sections.
    
    Args:
        request: The current HTTP request object, which contains the path and user information.

    Returns:
        dict: A dictionary with the key 'intra_menu', containing a list of menu items.
    """
    
    intra_menu = []  # Initialize the intra-page menu list
    current_path = request.path  # Get the current request path

    # If the user is on the accounts section
    if current_path.startswith('/accounts'):
        intra_menu = [
            {'name': 'User', 'url': '/accounts/user/', 'icon': 'fa-regular fa-user'},
            {'name': 'Email', 'url': '/accounts/email/', 'icon': 'fa-regular fa-envelope'},
            {'name': 'Password', 'url': '/accounts/password/change/', 'icon': 'fa-solid fa-key'},
        ]

    # If the user is on the dashboard section
    elif current_path.startswith('/dashboard'):
        intra_menu = [
            {'name': 'Main', 'url': '/dashboard/main/', 'icon': 'fas fa-home'},
        ]

    # If the user is in the portfolio section
    elif current_path.startswith('/portfolio'):
        portfolios = Portfolio.objects.filter(user=request.user)  # Fetch user's portfolios
        intra_menu = [
            {'name': 'View', 'url': '/portfolio/view/', 'icon': 'fa-solid fa-eye'},
            {'name': 'New', 'url': '/portfolio/new/', 'icon': 'fa-solid fa-plus'},
        ]
        # Add each portfolio to the menu
        for portfolio in portfolios:
            intra_menu.append({
                'name': portfolio.name,
                'url': f'/portfolio/{portfolio.pk}/',
                'icon': 'fa-solid fa-briefcase',
                'color': portfolio.color,  # Optionally include the portfolio color
            })

    # If the user is in the contact section
    elif current_path.startswith('/contact'):
        intra_menu = [
            {'name': 'View', 'url': '/contact/view/', 'icon': 'fa-solid fa-eye'},
        ]

    # If the user is in the metrics section
    elif current_path.startswith('/metrics'):
        portfolios = Portfolio.objects.filter(user=request.user)  # Fetch user's portfolios
        intra_menu = [
            {'name': 'View', 'url': '/metrics/view/', 'icon': 'fa-solid fa-eye'},
        ]
        # Add each portfolio under metrics section
        for portfolio in portfolios:
            intra_menu.append({
                'name': portfolio.name,
                'url': f'/metrics/{portfolio.pk}/',
                'icon': 'fa-solid fa-briefcase',
                'color': portfolio.color,
            })

    # If the user is in the operations section
    elif current_path.startswith('/operations'):
        intra_menu = [
            {'name': 'View', 'url': '/operations/view/', 'icon': 'fa-solid fa-eye'},
        ]

    # Return the intra-menu dictionary to be used in the template context
    return {'intra_menu': intra_menu}
