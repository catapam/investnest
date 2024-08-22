function activeMenu() {
    var currentPath = window.location.pathname + window.location.hash;

    // Normalize the path for "Home" cases
    if (currentPath === '/' || currentPath === '/#' || currentPath === '' || currentPath === '/#hero') {
        currentPath = '/#';
    }

    // Select all nav-links
    var navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    navLinks.forEach(link => {
        // Remove active class from all links
        link.classList.remove('active');

        // Check if the href ends with the current path (including fragment)
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
};

window.onload = function () {
    var showPopup = function (popupId) {
        var popup = document.getElementById(popupId);
        if (popup) {
            // Ensure the page stays at the top
            window.scrollTo({ top: 0, behavior: 'smooth' });
    
            // Show the popup
            popup.classList.add('show');
    
            // Hide the popup after 5 seconds
            setTimeout(function () {
                closePopup(popup);
            }, 3000);
    
            // Add event listener for close button
            popup.querySelector('.close-btn').addEventListener('click', function () {
                closePopup(popup);
            });
        }
    };
    
    var closePopup = function (popup) {
        popup.classList.remove('show');
    };
    
    // Show the success or error popup based on the condition
    ['success-popup', 'error-popup', 'info-popup', 'warning-popup', 'custom-popup'].forEach(function (popupId) {
        showPopup(popupId);
    });

    var popup = document.getElementById('popup');
    if (popup) {
        showPopup('popup');
    }

    // Function to check if any of the inner menu paths are active
    var activateDashboardMenu = function() {
        var currentPath = window.location.pathname;
        var innerMenuPaths = ['/dashboard/', '/portfolio/', '/metrics/', '/accounts/', '/contact/', '/operations/'];
        var dashboardLink = document.querySelector('.nav-link[href="/dashboard/"]');

        innerMenuPaths.forEach(function(path) {
            if (currentPath.startsWith(path)) {
                dashboardLink.classList.add('active');
            }
        });
    };

    // Activate the Dashboard menu if any inner menu paths are active
    activateDashboardMenu();

    // Update active menu item when the hash changes
    window.addEventListener('hashchange', activateDashboardMenu);
};
