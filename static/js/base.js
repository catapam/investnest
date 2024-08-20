window.onload = function () {
    var activeMenu = function () {
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

    var showPopup = function (popupId) {
        var popup = document.getElementById(popupId);
        if (popup) {
            // Ensure the page stays at the top
            window.scrollTo({ top: 0, behavior: 'smooth' });
            history.replaceState(null, null, '/#');
            activeMenu();
    
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
        activeMenu();
    };

    // Run the functions after the window is fully loaded
    activeMenu();
    
    // Show the success or error popup based on the condition
    showPopup('success-popup'); // Call this if there's a success
    showPopup('error-popup'); // Call this if there's an error

    // Update active menu item when the hash changes
    window.addEventListener('hashchange', activeMenu);

    // Check and update menu on initial load
    activeMenu();
};
