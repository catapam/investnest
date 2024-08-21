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

function initHomePageScripts() {
    var adjustHeightsAndAttachFlip = function () {
        var maxHeight = 0;
        var minHeight = 220;  // Set the minimum height
        var flipCardFronts = document.querySelectorAll('.flip-card-front');
        var flipCardBacks = document.querySelectorAll('.flip-card-back');
        var flipCardInners = document.querySelectorAll('.flip-card-inner');

        // Find the maximum height of all flip-card-front elements
        flipCardFronts.forEach(function (card) {
            var cardHeight = card.offsetHeight;
            if (cardHeight > maxHeight) {
                maxHeight = cardHeight;
            }
        });

        // Ensure the height is at least the minimum height
        maxHeight = Math.max(maxHeight, minHeight);

        // Set the height of all flip-card-front and flip-card-back elements to the maximum or minimum height
        flipCardFronts.forEach(function (card) {
            card.style.height = maxHeight + 'px';
        });

        flipCardBacks.forEach(function (card) {
            card.style.height = maxHeight + 'px';
        });

        // Set the height of all flip-card-inner elements to match the tallest card
        flipCardInners.forEach(function (card) {
            card.style.height = maxHeight + 'px';
        });

        // Set the max-height for card-text inside flip-card-back
        var cardTexts = document.querySelectorAll('.flip-card-back .card-body .card-text');
        cardTexts.forEach(function (text) {
            text.style.maxHeight = (maxHeight - text.closest('.card-body').offsetTop) * 0.6 + 'px';
        });

        // Attach flip event listeners
        document.querySelectorAll('.card-flip').forEach(card => {
            card.addEventListener('click', function () {
                card.querySelector('.flip-card-inner').classList.toggle('flipped');
            });
        });
    };

    var updateURLOnScroll = function (entries) {
        // Check if the page is at the top first
        if (window.scrollY === 0) {
            history.replaceState(null, null, '/#');
            activeMenu();
            return;
        }

        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Check if the entry is #hero and the scroll position is close to the top
                if (entry.target.id === 'hero' && window.scrollY <= 10) {
                    history.replaceState(null, null, '/#');
                } else {
                    history.replaceState(null, null, '#' + entry.target.id);
                }
                activeMenu();
            }
        });
    };

    var updateForFooter = function (entries) {
        var currentPath = window.location.pathname;

        // Only update if the current path is home "/"
        if (currentPath === '/' || currentPath === '/#') {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Force the URL to #contact when the footer is visible
                    history.replaceState(null, null, '#contact');
                    activeMenu();
                }
            });
        }
    };

    var collapseMobileMenu = function () {
        var navbarToggler = document.querySelector('.navbar-toggler');
        var navbarCollapse = document.querySelector('.navbar-collapse');

        if (navbarCollapse.classList.contains('show')) {
            console.log('Collapsing mobile menu');
            navbarToggler.click();
        } else {
            console.log('Mobile menu already collapsed');
        }
    };

    // Run the functions after the window is fully loaded
    adjustHeightsAndAttachFlip();

    // Intersection Observer to detect section visibility
    var observer = new IntersectionObserver(updateURLOnScroll, {
        rootMargin: '-30% 0px -70% 0px',  // Adjust this value to trigger closer to the top of the viewport
        threshold: [0, 0.1, 0.9]  // Multiple thresholds to detect entry and exit accurately
    });

    // Observe each section you want to track
    document.querySelectorAll('section[id]').forEach(section => {
        observer.observe(section);
    });

    // Intersection Observer for the footer
    var footerObserver = new IntersectionObserver(updateForFooter, {
        rootMargin: '0px 0px 0px 0px',
        threshold: 0.1  // Trigger when 10% of the footer is visible
    });

    // Observe the footer
    footerObserver.observe(document.querySelector('footer'));

    // Update active menu item when the hash changes
    window.addEventListener('hashchange', activeMenu);

    // Attach event listener to nav links to collapse the mobile menu on click
    document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
        link.addEventListener('click', function () {
            collapseMobileMenu();
        });
    });

    // Check and update menu on initial load
    activeMenu();
}

// Execute the function directly (without overwriting window.onload)
initHomePageScripts();
