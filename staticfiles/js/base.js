/**
 * Displays a popup by adding the 'show' class to the element with the specified popupId.
 * The popup is automatically closed after 3 seconds or when the close button is clicked.
 *
 * @param {string} popupId - The ID of the popup element to be displayed.
 */
function showPopup(popupId) {
    var popup = document.getElementById(popupId); // Select the popup element by ID

    if (popup) {
        // Scroll to the top of the page smoothly
        window.scrollTo({ top: 0, behavior: 'smooth' });

        // Show the popup by adding the 'show' class
        popup.classList.add('show');

        // Set a timeout to hide the popup after 3 seconds (3000 ms)
        setTimeout(function () {
            closePopup(popup); // Close the popup automatically after the time expires
        }, 3000);

        // Add event listener to the close button inside the popup to close it on click
        var closeButton = popup.querySelector('.close-btn');
        if (closeButton) {
            closeButton.addEventListener('click', function () {
                closePopup(popup);
            });
        }
    }
}

/**
 * Closes the given popup by removing the 'show' class.
 *
 * @param {HTMLElement} popup - The popup element to close.
 */
function closePopup(popup) {
    popup.classList.remove('show'); // Hide the popup by removing the 'show' class
}

/**
 * Initializes the base functionality for popups.
 * It attempts to display popups by their IDs if they are present on the page.
 */
function initBaseJS() {
    var popupIds = ['success-popup', 'error-popup', 'info-popup', 'warning-popup', 'custom-popup'];

    // Loop through each popup ID and attempt to show it if the element exists
    popupIds.forEach(function (popupId) {
        showPopup(popupId);
    });

    // Additional check for a generic 'popup' ID element and show it if found
    var popup = document.getElementById('popup');
    if (popup) {
        showPopup('popup');
    }
}

// Run the initialization function when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    initBaseJS();
});
