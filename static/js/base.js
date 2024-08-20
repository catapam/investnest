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
    showPopup('success-popup'); // Call this if there's a success
    showPopup('error-popup'); // Call this if there's an error
    var popup = document.getElementById('popup');
    if (popup) {
        showPopup('popup');
    }

    // Update active menu item when the hash changes
    window.addEventListener('hashchange', activeMenu);
};
