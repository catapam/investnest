document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggle-btn');
    const mainContent = document.getElementById('dashboard-content');

    // Function to handle sidebar collapse/expand based on screen width
    function handleScreenResize() {
        if (window.innerWidth < 768) {
            sidebar.classList.add('collapsed');
            mainContent.classList.add('collapsed');
            toggleBtn.querySelector('i').classList.remove('fa-arrow-left');
            toggleBtn.querySelector('i').classList.add('fa-arrow-right');
        } else {
            sidebar.classList.remove('collapsed');
            mainContent.classList.remove('collapsed');
            toggleBtn.querySelector('i').classList.remove('fa-arrow-right');
            toggleBtn.querySelector('i').classList.add('fa-arrow-left');
        }
    }

    // Run the function on page load and screen resize
    handleScreenResize();
    window.addEventListener('resize', handleScreenResize);

    // Toggle button click event
    toggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('collapsed');
        toggleBtn.querySelector('i').classList.toggle('fa-arrow-left');
        toggleBtn.querySelector('i').classList.toggle('fa-arrow-right');
    });

    // Function to check if any of the inner menu paths are active
    var activateInnerDashboardMenu = function() {
        var currentPath = window.location.pathname;
        var innerMenuPaths = ['/dashboard/', '/portfolio/', '/metrics/', '/accounts/', '/contact/', '/operations/', '/accounts/email/', '/accounts/password/change/'];
    
        innerMenuPaths.forEach(function(path) {
            // Select all matching links
            var links = document.querySelectorAll(`[href="${path}"].nav-link`);
            links.forEach(function(link) {
                // Check if the link is inside an element with the class 'option-menu'
                var isInOptionMenu = link.closest('.option-menu') !== null;
    
                if (isInOptionMenu) {
                    // For links inside 'option-menu', check if the path is an exact match
                    if (currentPath === path) {
                        link.classList.add('active');
                    }
                } else {
                    // For all other links, check if the path starts with the link's href
                    if (currentPath.startsWith(path)) {
                        link.classList.add('active');
                    }
                }
            });
        });
    };

    // Activate the Dashboard menu if any inner menu paths are active
    activateInnerDashboardMenu();

    activeMenu();
});

