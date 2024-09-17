/**
 * Updates the active state of the navigation menu based on the current URL path and hash.
 */
function activeMenu() {
    var currentPath = window.location.pathname + window.location.hash;

    // Normalize the path for "Home" cases (e.g., '/', '/#', etc.)
    if (currentPath === '/' || currentPath === '/#' || currentPath === '' || currentPath === '/#hero') {
        currentPath = '/#';
    }

    // Select all navigation links in the navbar
    var navLinks = document.querySelectorAll('.navbar-nav .nav-link');

    // Loop through each nav link and update its 'active' class based on the current path
    navLinks.forEach(function (link) {
        link.classList.remove('active'); // Remove 'active' from all links

        // Add 'active' to the link that matches the current path
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

/**
 * Adjusts the height of flip cards based on the tallest card and attaches flip events.
 */
function adjustHeights() {
    var maxHeight = 0; // To store the maximum height
    var minHeight = 220; // Set the minimum height for flip cards

    // Get all flip-card elements
    var flipCardFronts = document.querySelectorAll('.flip-card-front');
    var flipCardBacks = document.querySelectorAll('.flip-card-back');
    var flipCardInners = document.querySelectorAll('.flip-card-inner');

    // Find the maximum height of the flip cards
    flipCardFronts.forEach(function (card) {
        var cardHeight = card.offsetHeight;
        if (cardHeight > maxHeight) {
            maxHeight = cardHeight;
        }
    });

    // Ensure the max height is at least the minimum height
    maxHeight = Math.max(maxHeight, minHeight);

    // Set the height for flip-card-front, flip-card-back, and flip-card-inner elements
    flipCardFronts.forEach(function (card) {
        card.style.height = maxHeight + 'px';
    });
    flipCardBacks.forEach(function (card) {
        card.style.height = maxHeight + 'px';
    });
    flipCardInners.forEach(function (card) {
        card.style.height = maxHeight + 'px';
    });

    // Adjust the text height for card-text inside flip-card-back
    adjustTextHeight(maxHeight);
}

/**
 * Adjusts the max-height of text elements inside flip-card-back elements.
 * @param {number} maxHeight - The maximum height of the flip cards.
 */
function adjustTextHeight(maxHeight) {
    var cardTexts = document.querySelectorAll('.flip-card-back .card-body .card-text');
    cardTexts.forEach(function (text) {
        text.style.maxHeight = (maxHeight - text.closest('.card-body').offsetTop) * 0.6 + 'px';
    });
}

/**
 * Attaches flip events to the flip cards.
 * When a card is clicked, it toggles the 'flipped' class to animate the flip.
 */
function attachFlipEvents() {
    document.querySelectorAll('.flip-card-inner').forEach(function (card) {
        card.addEventListener('click', function () {
            card.classList.toggle('flipped'); // Toggle the 'flipped' class
        });
    });
}

/**
 * Updates the URL hash based on the scroll position and activates the corresponding menu item.
 * @param {IntersectionObserverEntry[]} entries - The list of observed elements.
 */
function updateURLOnScroll(entries) {
    if (window.scrollY === 0) {
        history.replaceState(null, null, '/#'); // Reset the URL when scrolled to the top
        activeMenu(); // Update the active menu
        return;
    }

    entries.forEach(function (entry) {
        if (entry.isIntersecting) {
            // Update the URL hash based on the visible section
            if (entry.target.id === 'hero' && window.scrollY <= 10) {
                history.replaceState(null, null, '/#');
            } else {
                history.replaceState(null, null, '#' + entry.target.id);
            }
            activeMenu(); // Update the active menu
        }
    });
}

/**
 * Updates the URL to "#contact" when the footer becomes visible.
 * @param {IntersectionObserverEntry[]} entries - The list of observed elements.
 */
function updateForFooter(entries) {
    var currentPath = window.location.pathname;
    if (currentPath === '/' || currentPath === '/#') {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                history.replaceState(null, null, '#contact'); // Set the URL to #contact
                activeMenu(); // Update the active menu
            }
        });
    }
}

/**
 * Collapses the mobile menu when a navigation link is clicked.
 */
function collapseMobileMenu() {
    var navbarToggler = document.querySelector('.navbar-toggler');
    var navbarCollapse = document.querySelector('.navbar-collapse');

    // Check if the mobile menu is open and collapse it
    if (navbarCollapse.classList.contains('show')) {
        navbarToggler.click(); // Trigger the click event to close the menu
    }
}

/**
 * Initializes the intersection observers to track section and footer visibility.
 */
function initializeObservers() {
    var observer = new IntersectionObserver(updateURLOnScroll, {
        rootMargin: '-30% 0px -70% 0px', // Adjust margins for triggering
        threshold: [0, 0.1, 0.9] // Trigger at different scroll points
    });

    // Observe each section by its ID for URL updates
    document.querySelectorAll('section[id]').forEach(function (section) {
        observer.observe(section);
    });

    // Observe the footer to update URL when visible
    var footerObserver = new IntersectionObserver(updateForFooter, {
        rootMargin: '0px 0px 0px 0px', // No margin adjustments
        threshold: 0.1 // Trigger when 10% of the footer is visible
    });

    footerObserver.observe(document.querySelector('footer'));
}

/**
 * Initializes event listeners for mobile menu and hash changes.
 */
function initializeEventListeners() {
    // Add event listener to each nav-link to collapse the mobile menu on click
    document.querySelectorAll('.navbar-nav .nav-link').forEach(function (link) {
        link.addEventListener('click', collapseMobileMenu);
    });

    // Update the active menu when the URL hash changes
    window.addEventListener('hashchange', activeMenu);
}

// Main initialization function that runs when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    adjustHeights(); // Adjust flip card heights
    attachFlipEvents(); // Attach flip card events
    initializeObservers(); // Set up scroll observers
    initializeEventListeners(); // Set up event listeners
    activeMenu(); // Set the active menu based on the current URL
});
