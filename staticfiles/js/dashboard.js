document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggle-btn');
    const mainContent = document.getElementById('dashboard-content');
    const optionMenu = document.querySelector('.option-menu');
    const scrollButtonLeft = document.querySelector('.scroll-button-left');
    const scrollButtonRight = document.querySelector('.scroll-button-right');
    const optionMenuWrapper = document.querySelector('.option-menu-wrapper');

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

    // Function to check if any of the inner menu paths are active
    var activateInnerDashboardMenu = function () {
        var currentPath = window.location.pathname;
        var innerMenuPaths = ['/dashboard/', '/portfolio/', '/metrics/', '/accounts/', '/contact/', '/operations/', '/accounts/email/', '/accounts/password/change/'];

        innerMenuPaths.forEach(function (path) {
            // Select all matching links
            var links = document.querySelectorAll(`[href="${path}"].nav-link`);
            links.forEach(function (link) {
                // Check if the link is inside an element with the class 'option-menu'
                var isInOptionMenu = link.closest('.option-menu') !== null;

                if (isInOptionMenu) {
                    // For links inside 'option-menu', check if the path is an exact match
                    if (currentPath === path) {
                        link.classList.add('active');
                        // Scroll the active item into view, centered
                        scrollActiveItemIntoView(link);
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

    if (typeof activeMenu === 'function') {
        activeMenu();
    }

    // Function to scroll the active menu item into view, centered
    function scrollActiveItemIntoView(item) {
        const menuWidth = optionMenu.clientWidth;
        const itemLeft = item.offsetLeft;
        const itemWidth = item.offsetWidth;

        const scrollPosition = itemLeft - (menuWidth / 2) + (itemWidth / 2);
        optionMenu.scrollTo({
            left: scrollPosition,
            behavior: 'smooth'
        });
    }

    // Function to check which elements are visible in the scrollable container
    function updateScrollButtonsAndFadedItems() {
        const scrollLeft = optionMenu.scrollLeft;
        const visibleWidth = optionMenu.clientWidth;
        const maxScrollLeft = optionMenu.scrollWidth - visibleWidth;

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
        const menuItems = optionMenu.querySelectorAll('.nav-item');
        menuItems.forEach(function (item, index) {
            const itemLeft = item.offsetLeft - scrollLeft;
            const itemRight = itemLeft + item.offsetWidth;

            // Adjust visibility calculation to account for boundary conditions
            const isPartiallyVisible = (itemLeft < 0 && index !== 0) || (itemRight > visibleWidth && index !== menuItems.length - 1);

            if (isPartiallyVisible) {
                item.classList.add('faded');
            } else {
                item.classList.remove('faded');
            }
        });
    }

    // Function to scroll the option menu to the right
    function scrollMenuRight() {
        const menuWidth = optionMenu.clientWidth;
        optionMenu.scrollBy({ left: menuWidth / 2, behavior: 'smooth' });
        setTimeout(updateScrollButtonsAndFadedItems, 300);
    }

    // Function to scroll the option menu to the left
    function scrollMenuLeft() {
        const menuWidth = optionMenu.clientWidth;
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
