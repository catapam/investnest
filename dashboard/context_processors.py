from portfolio.models import Portfolio


class IntraMenuProcessorClass:
    """
    Class-based context processor to generate an intra-page menu based
    on the current URL path.

    The menu is tailored to the specific section of the application
    the user is in.

    This class is used for rendering intra-navigation menus dynamically
    across different sections.

    Args:
        request: The current HTTP request object,
        which contains the path and user information.

    Returns:
        dict: A dictionary with the key 'intra_menu',
        containing a list of menu items.
    """

    def __init__(self, request):
        """
        Initializes the IntraMenuProcessor with the request object.
        """
        self.request = request
        self.intra_menu = []
        self.current_path = request.path  # Get the current request path

    def get_intra_menu(self):
        """
        Generates the intra-page menu based on the current URL path.

        Returns:
            dict: A dictionary with the key 'intra_menu',
            containing a list of menu items.
        """
        # Call the appropriate handler based on the current path
        if self.current_path.startswith('/accounts'):
            self._handle_accounts()
        elif self.current_path.startswith('/dashboard'):
            self._handle_dashboard()
        elif self.current_path.startswith('/portfolio'):
            self._handle_portfolio()
        elif self.current_path.startswith('/contact'):
            self._handle_contact()
        elif self.current_path.startswith('/metrics'):
            self._handle_metrics()
        elif self.current_path.startswith('/operations'):
            self._handle_operations()

        # Return the generated menu
        return {'intra_menu': self.intra_menu}

    def _handle_accounts(self):
        """Generates the intra-menu for the accounts section."""
        self.intra_menu = [
            {
                'name': 'User',
                'url': '/accounts/user/',
                'icon': 'fa-regular fa-user',
            },
            {
                'name': 'Email',
                'url': '/accounts/email/',
                'icon': 'fa-regular fa-envelope',
            },
            {
                'name': 'Password',
                'url': '/accounts/password/change/',
                'icon': 'fa-solid fa-key',
            },
        ]

    def _handle_dashboard(self):
        """Generates the intra-menu for the dashboard section."""
        self.intra_menu = [
            {
                'name': 'Main',
                'url': '/dashboard/view/',
                'icon': 'fas fa-home',
            },
        ]

    def _handle_portfolio(self):
        """Generates the intra-menu for the portfolio section."""
        portfolios = Portfolio.objects.filter(user=self.request.user)
        self.intra_menu = [
            {
                'name': 'View',
                'url': '/portfolio/view/',
                'icon': 'fa-solid fa-eye',
            },
            {
                'name': 'New',
                'url': '/portfolio/new/',
                'icon': 'fa-solid fa-plus',
            },
        ]
        for portfolio in portfolios:
            self.intra_menu.append({
                'name': portfolio.name,
                'url': f'/portfolio/{portfolio.pk}/',
                'icon': 'fa-solid fa-briefcase',
                'color': portfolio.color,
            })

    def _handle_contact(self):
        """Generates the intra-menu for the contact section."""
        self.intra_menu = [
            {
                'name': 'View',
                'url': '/contact/view/',
                'icon': 'fa-solid fa-eye',
            },
        ]

    def _handle_metrics(self):
        """Generates the intra-menu for the metrics section."""
        portfolios = Portfolio.objects.filter(user=self.request.user)
        self.intra_menu = [
            {
                'name': 'View',
                'url': '/metrics/view/',
                'icon': 'fa-solid fa-eye',
            },
        ]
        for portfolio in portfolios:
            self.intra_menu.append({
                'name': portfolio.name,
                'url': f'/metrics/{portfolio.pk}/',
                'icon': 'fa-solid fa-briefcase',
                'color': portfolio.color,
            })

    def _handle_operations(self):
        """Generates the intra-menu for the operations section."""
        self.intra_menu = [
            {
                'name': 'View',
                'url': '/operations/view/',
                'icon': 'fa-solid fa-eye',
            },
        ]


# To use the class as a context processor, initialize it and return the menu:
def IntraMenuProcessor(request):
    processor = IntraMenuProcessorClass(request)
    return processor.get_intra_menu()
