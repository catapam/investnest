document.addEventListener('DOMContentLoaded', function () {
    var sidebar = document.getElementById('sidebar');
    var toggleBtn = document.getElementById('toggle-btn');
    var mainContent = document.getElementById('dashboard-content');
    var optionMenu = document.querySelector('.option-menu');
    var scrollButtonLeft = document.querySelector('.scroll-button-left');
    var scrollButtonRight = document.querySelector('.scroll-button-right');
    var optionMenuWrapper = document.querySelector('.option-menu-wrapper');

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
    toggleBtn.addEventListener('click', function () {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('collapsed');
        toggleBtn.querySelector('i').classList.toggle('fa-arrow-left');
        toggleBtn.querySelector('i').classList.toggle('fa-arrow-right');
    });

    var activateInnerDashboardMenu = function () {
        var currentPath = window.location.pathname;
    
        // Activate the broader menu links with partial match
        var broadMenuLinks = document.querySelectorAll('.sidebar .nav-link');
        broadMenuLinks.forEach(function (link) {
            var linkPath = link.getAttribute('href');
            // Partial match for the broader menu
            if (currentPath.startsWith(linkPath)) {
                link.classList.add('active');
            }
        });
    
        // Activate the inner menu links with exact match
        var innerMenuLinks = document.querySelectorAll('.option-menu .nav-link');
        innerMenuLinks.forEach(function (link) {
            var linkPath = link.getAttribute('href');
            // Exact match for the inner menu
            if (currentPath.startsWith(linkPath)) {
                link.classList.add('active');
                scrollActiveItemIntoView(link);
            }
        });
    };

    // Activate the Dashboard menu if any inner menu paths are active
    activateInnerDashboardMenu();

    if (typeof activeMenu === 'function') {
        activeMenu();
    }

    // Function to scroll the active menu item into view, centered
    function scrollActiveItemIntoView(item) {
        var menuWidth = optionMenu.clientWidth;
        var itemLeft = item.offsetLeft;
        var itemWidth = item.offsetWidth;

        var scrollPosition = itemLeft - (menuWidth / 2) + (itemWidth / 2);
        optionMenu.scrollTo({
            left: scrollPosition,
            behavior: 'smooth'
        });
    }

    // Function to check which elements are visible in the scrollable container
    function updateScrollButtonsAndFadedItems() {
        var scrollLeft = optionMenu.scrollLeft;
        var visibleWidth = optionMenu.clientWidth;
        var maxScrollLeft = optionMenu.scrollWidth - visibleWidth;

        // Show or hide the left scroll button
        if (scrollLeft > 0) {
            scrollButtonLeft.style.display = 'block';
        } else {
            scrollButtonLeft.style.display = 'none';
        }

        // Show or hide the right scroll button
        if (scrollLeft < maxScrollLeft - 1) { // Slightly adjusting to prevent early hiding
            scrollButtonRight.style.display = 'block';
        } else {
            scrollButtonRight.style.display = 'none';
        }

        // Apply the 'faded' class to items that are partially hidden
        var menuItems = optionMenu.querySelectorAll('.nav-item');
        menuItems.forEach(function (item, index) {
            var itemLeft = item.offsetLeft - scrollLeft;
            var itemRight = itemLeft + item.offsetWidth;

            // Adjust visibility calculation to account for boundary conditions
            var isPartiallyVisible = (itemLeft < 0 && index !== 0) || (itemRight > visibleWidth && index !== menuItems.length - 1);

            if (isPartiallyVisible) {
                item.classList.add('faded');
            } else {
                item.classList.remove('faded');
            }
        });
    }

    // Function to scroll the option menu to the right
    function scrollMenuRight() {
        var menuWidth = optionMenu.clientWidth;
        optionMenu.scrollBy({ left: menuWidth / 2, behavior: 'smooth' });
        setTimeout(updateScrollButtonsAndFadedItems, 300);
    }

    // Function to scroll the option menu to the left
    function scrollMenuLeft() {
        var menuWidth = optionMenu.clientWidth;
        optionMenu.scrollBy({ left: -menuWidth / 2, behavior: 'smooth' });
        setTimeout(updateScrollButtonsAndFadedItems, 300);
    }

    // Update scroll button visibility and faded items on load and resize
    updateScrollButtonsAndFadedItems();
    window.addEventListener('resize', updateScrollButtonsAndFadedItems);

    // Scroll the menu when the buttons are clicked
    scrollButtonRight.addEventListener('click', scrollMenuRight);
    scrollButtonLeft.addEventListener('click', scrollMenuLeft);

    // Additional check to hide the scroll button if the menu reaches the end
    optionMenu.addEventListener('scroll', updateScrollButtonsAndFadedItems);

    // Add click listeners to the option menu wrapper to update the fading layout
    optionMenuWrapper.addEventListener('click', function () {
        updateScrollButtonsAndFadedItems();
    });
});
