/**
 * Toggles the sidebar collapse/expand and updates the toggle button icon.
 */
function handleSidebarToggle() {
    var sidebar = document.getElementById('sidebar');
    var toggleBtn = document.getElementById('toggle-btn');
    var mainContent = document.getElementById('dashboard-content');

    // Toggle the 'collapsed' class on the sidebar and main content
    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('collapsed');

    // Toggle the icon between left and right arrow
    toggleBtn.querySelector('i').classList.toggle('fa-arrow-left');
    toggleBtn.querySelector('i').classList.toggle('fa-arrow-right');

    // Check if screen width is smaller than 768px
    colapsableMenuPortfolio();
}

/**
 * Toggles the visibility of the portfolio menu on smaller screens (< 768px).
 * Hides or shows the portfolio menu based on the current path and the sidebar's collapsed state.
 */
function colapsableMenuPortfolio() {
    var currentPath = window.location.pathname;

    // Regular expressions to check if the path starts with /portfolio/ or /metrics/ followed by at least one number
    var portfolioRegex = /^\/portfolio\/\d+(\/.*)?/;
    var metricsRegex = /^\/metrics\/\d+(\/.*)?/;

    // If the current path matches either regex
    if (portfolioRegex.test(currentPath) || metricsRegex.test(currentPath)) {
        // Select the portfolio menu elements
        var portfolioMenuCollapse = document.querySelector('.portfolio-menu-collapse');
        var portfolioMenuWide = document.querySelector('.portfolio-menu-wide');
        var sidebar = document.getElementById('sidebar'); // Ensure the sidebar element is selected

        // Check if screen width is smaller than 768px
        if (window.innerWidth < 768) {
            // Check the sidebar's collapsed state and adjust the visibility of portfolio menus accordingly
            if (sidebar.classList.contains('collapsed')) {
                // When sidebar is collapsed, show the collapsed portfolio menu and hide the wide menu
                portfolioMenuCollapse.style.display = 'block';
                portfolioMenuWide.style.display = 'none';
            } else {
                // When sidebar is expanded, hide the collapsed portfolio menu and show the wide menu
                portfolioMenuCollapse.style.display = 'none';
                portfolioMenuWide.style.display = 'none';
            }
        } else{
            portfolioMenuCollapse.style.display = 'none';
            portfolioMenuWide.style.display = 'block';
        }
    }
}

/**
 * Adjusts the sidebar and main content layout based on screen width.
 * Collapses the sidebar on smaller screens (< 768px) and expands it on larger screens.
 */
function handleScreenResize() {
    var sidebar = document.getElementById('sidebar');
    var toggleBtn = document.getElementById('toggle-btn');
    var mainContent = document.getElementById('dashboard-content');

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

    colapsableMenuPortfolio();
}

/**
 * Activates the broader dashboard menu if the current URL path matches any of the inner menu paths.
 */
function activateDashboardMenu() {
    var currentPath = window.location.pathname;
    var innerMenuPaths = ['/dashboard/', '/portfolio/', '/metrics/', '/accounts/', '/contact/', '/operations/'];
    var dashboardLink = document.querySelector('.nav-link[href="/dashboard/"]');

    // Check if the current path starts with any of the inner menu paths and activate the dashboard menu
    innerMenuPaths.forEach(function (path) {
        if (currentPath.startsWith(path)) {
            dashboardLink.classList.add('active');
        }
    });
}

/**
 * Activates the inner dashboard menu links based on the current path.
 * Scrolls the active link into view for better visibility.
 */
function activateInnerDashboardMenu() {
    var currentPath = window.location.pathname;
    var broadMenuLinks = document.querySelectorAll('.sidebar .nav-link');
    var innerMenuLinks = document.querySelectorAll('.option-menu .nav-link');

    // Activate the sidebar links that partially match the current path
    broadMenuLinks.forEach(function (link) {
        var linkPath = link.getAttribute('href');
        if (currentPath.startsWith(linkPath)) {
            link.classList.add('active');
        }
    });

    // Activate the inner option menu links that exactly match the current path
    innerMenuLinks.forEach(function (link) {
        var linkPath = link.getAttribute('href');
        if (currentPath.startsWith(linkPath)) {
            link.classList.add('active');
            scrollActiveItemIntoView(link); // Scroll the active item into view
        }
    });
}

/**
 * Scrolls the active menu item into view, ensuring it is centered in the option menu.
 * @param {HTMLElement} item - The active menu item to scroll into view.
 */
function scrollActiveItemIntoView(item) {
    var optionMenu = document.querySelector('.option-menu');
    var menuWidth = optionMenu.clientWidth;
    var itemLeft = item.offsetLeft;
    var itemWidth = item.offsetWidth;

    var scrollPosition = itemLeft - (menuWidth / 2) + (itemWidth / 2);
    optionMenu.scrollTo({
        left: scrollPosition,
        behavior: 'smooth'
    });
}

/**
 * Updates the visibility of scroll buttons and applies the 'faded' class to items that are partially visible.
 */
function updateScrollButtons() {
    var optionMenu = document.querySelector('.option-menu');
    var scrollButtonLeft = document.querySelector('.scroll-button-left');
    var scrollButtonRight = document.querySelector('.scroll-button-right');
    var scrollLeft = optionMenu.scrollLeft;
    var visibleWidth = optionMenu.clientWidth;
    var maxScrollLeft = optionMenu.scrollWidth - visibleWidth;

    // Show or hide the left scroll button based on the scroll position
    scrollButtonLeft.style.display = scrollLeft > 0 ? 'block' : 'none';

    // Show or hide the right scroll button based on the remaining scrollable content
    scrollButtonRight.style.display = scrollLeft < maxScrollLeft - 1 ? 'block' : 'none';
}

/**
 * Scrolls the option menu to the right by half of its width.
 */
function scrollMenuRight() {
    var optionMenu = document.querySelector('.option-menu');
    var menuWidth = optionMenu.clientWidth;
    optionMenu.scrollBy({ left: menuWidth / 2, behavior: 'smooth' });
    setTimeout(updateScrollButtons, 300); // Update buttons and faded items after scrolling
}

/**
 * Scrolls the option menu to the left by half of its width.
 */
function scrollMenuLeft() {
    var optionMenu = document.querySelector('.option-menu');
    var menuWidth = optionMenu.clientWidth;
    optionMenu.scrollBy({ left: -menuWidth / 2, behavior: 'smooth' });
    setTimeout(updateScrollButtons, 300); // Update buttons and faded items after scrolling
}

/**
 * Initializes event listeners for the sidebar, menu scroll, and resizing behaviors.
 */
function initializeEventListeners() {
    var toggleBtn = document.getElementById('toggle-btn');
    var scrollButtonLeft = document.querySelector('.scroll-button-left');
    var scrollButtonRight = document.querySelector('.scroll-button-right');
    var optionMenuWrapper = document.querySelector('.option-menu-wrapper');

    //Screenresize
    window.addEventListener('resize', handleScreenResize);

    // Attach click event listener to the sidebar toggle button
    toggleBtn.addEventListener('click', handleSidebarToggle);

    // Attach click event listeners to the scroll buttons
    scrollButtonRight.addEventListener('click', scrollMenuRight);
    scrollButtonLeft.addEventListener('click', scrollMenuLeft);

    // Update scroll buttons and faded items on scroll and window resize
    document.querySelector('.option-menu').addEventListener('scroll', updateScrollButtons);
    window.addEventListener('resize', updateScrollButtons);

    // Update scroll buttons and faded items when clicking inside the option menu wrapper
    optionMenuWrapper.addEventListener('click', updateScrollButtons);
}

// Execute the main initialization functions after DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    handleScreenResize();
    initializeEventListeners();
    activateDashboardMenu();
    activateInnerDashboardMenu();
    updateScrollButtons();
});