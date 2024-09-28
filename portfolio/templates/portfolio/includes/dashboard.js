/**
 * Toggles the sidebar collapse/expand and updates the toggle button icon.
 */
function handleSidebarToggle() {
    var sidebar = document.getElementById('sidebar');
    var toggleBtn = document.getElementById('toggle-btn');
    var mainContent = document.getElementById('dashboard-content');
    var currentPath = window.location.pathname;

    // Toggle the 'collapsed' class on the sidebar and main content
    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('collapsed');

    // Toggle the icon between left and right arrow
    toggleBtn.querySelector('i').classList.toggle('fa-arrow-left');
    toggleBtn.querySelector('i').classList.toggle('fa-arrow-right');

    // Check if screen width is smaller than 768px
    if (window.innerWidth < 768) {
        // Check if the path starts with /portfolio or /metrics
        if (currentPath.startsWith('/portfolio') || currentPath.startsWith('/metrics')) {
            var portfolioMenuCollapse = document.querySelector('.portfolio-menu-collapse');
            var portfolioMenuWide = document.querySelector('.font-weight: 400');

            if (sidebar.classList.contains('collapsed')) {
                // Hide the portfolio menu
                portfolioMenuCollapse.style.display = 'block';
                portfolioMenuWide.style.display = 'none';
            } else {
                // Show the portfolio menu
                portfolioMenuCollapse.style.display = 'none';
                portfolioMenuWide.style.display = 'block';
            }
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
function updateScrollButtonsAndFadedItems() {
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

    // Add or remove the 'faded' class to items based on their visibility
    var menuItems = optionMenu.querySelectorAll('.nav-item');
    menuItems.forEach(function (item, index) {
        var itemLeft = item.offsetLeft - scrollLeft;
        var itemRight = itemLeft + item.offsetWidth;

        // Check if the item is partially visible and apply the 'faded' class accordingly
        var isPartiallyVisible = (itemLeft < 0 && index !== 0) || (itemRight > visibleWidth && index !== menuItems.length - 1);
        item.classList.toggle('faded', isPartiallyVisible);
    });
}

/**
 * Scrolls the option menu to the right by half of its width.
 */
function scrollMenuRight() {
    var optionMenu = document.querySelector('.option-menu');
    var menuWidth = optionMenu.clientWidth;
    optionMenu.scrollBy({ left: menuWidth / 2, behavior: 'smooth' });
    setTimeout(updateScrollButtonsAndFadedItems, 300); // Update buttons and faded items after scrolling
}

/**
 * Scrolls the option menu to the left by half of its width.
 */
function scrollMenuLeft() {
    var optionMenu = document.querySelector('.option-menu');
    var menuWidth = optionMenu.clientWidth;
    optionMenu.scrollBy({ left: -menuWidth / 2, behavior: 'smooth' });
    setTimeout(updateScrollButtonsAndFadedItems, 300); // Update buttons and faded items after scrolling
}

/**
 * Initializes event listeners for the sidebar, menu scroll, and resizing behaviors.
 */
function initializeEventListeners() {
    var toggleBtn = document.getElementById('toggle-btn');
    var scrollButtonLeft = document.querySelector('.scroll-button-left');
    var scrollButtonRight = document.querySelector('.scroll-button-right');
    var optionMenuWrapper = document.querySelector('.option-menu-wrapper');

    // Attach click event listener to the sidebar toggle button
    toggleBtn.addEventListener('click', handleSidebarToggle);

    // Attach click event listeners to the scroll buttons
    scrollButtonRight.addEventListener('click', scrollMenuRight);
    scrollButtonLeft.addEventListener('click', scrollMenuLeft);

    // Update scroll buttons and faded items on scroll and window resize
    document.querySelector('.option-menu').addEventListener('scroll', updateScrollButtonsAndFadedItems);
    window.addEventListener('resize', updateScrollButtonsAndFadedItems);

    // Update scroll buttons and faded items when clicking inside the option menu wrapper
    optionMenuWrapper.addEventListener('click', updateScrollButtonsAndFadedItems);
}

// Execute the main initialization functions after DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    handleScreenResize();
    initializeEventListeners();
    activateDashboardMenu();
    activateInnerDashboardMenu();
    updateScrollButtonsAndFadedItems();
});
