
/**
 * Toggles between display and edit modes for the portfolio header.
 * @param {number} portfolioId - The ID of the portfolio to edit.
 * @param {boolean} editMode - Set to true to enable edit mode, false to return to display mode.
 */
function togglePortfolioEditMode(portfolioId, editMode = true) {
    var row = document.getElementById('portfolio-header');
    var displayModeElements = row.querySelectorAll('.display-mode');
    var editModeElements = row.querySelectorAll('.edit-mode');
    var editButton = row.querySelector('.edit-toggle');
    var deleteButton = row.querySelector('.delete-toggle');
    var saveButton = row.querySelector('.save-toggle');
    var cancelButton = row.querySelector('.cancel-toggle');
    var metricsButton = row.querySelector('.metrics-toggle');

    // Toggle between edit and display modes
    if (editMode) {
        displayModeElements.forEach(element => element.style.display = 'none');
        editModeElements.forEach(element => element.style.display = 'block');
        editButton.style.display = 'none';
        deleteButton.style.display = 'none';
        metricsButton.style.display = 'none';
        saveButton.style.display = 'block';
        cancelButton.style.display = 'block';
    } else {
        displayModeElements.forEach(element => element.style.display = 'block');
        editModeElements.forEach(element => element.style.display = 'none');
        editButton.style.display = 'block';
        deleteButton.style.display = 'block';
        metricsButton.style.display = 'block';
        saveButton.style.display = 'none';
        cancelButton.style.display = 'none';
    }
}

/**
 * Sends a POST request to save the changes made to the portfolio.
 * @param {number} portfolioId - The ID of the portfolio to save.
 */
function savePortfolio(portfolioId) {
    var row = document.getElementById('portfolio-header');
    var name = row.querySelector('input[name="name"]').value;
    var description = row.querySelector('input[name="description"]').value;
    var color = row.querySelector('input[name="color"]').value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Send the portfolio update request to the server
    fetch(`/portfolio/${portfolioId}/edit/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,  // Include CSRF token for security
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            'name': name,
            'description': description,
            'color': color,
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        return response.json().then(err => { throw err; });
    })
    .then(data => {
        if (data.status === 'success') {
            location.reload();  // Reload the page on success to reflect the changes
        } else {
            console.error('Error:', data.errors);
            alert('Failed to save the portfolio changes. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while saving the portfolio. Please try again.');
    });
}

/**
 * Event listener for DOMContentLoaded to ensure the page is fully loaded before running scripts.
 */
document.addEventListener('DOMContentLoaded', function () {
    var colorPicker = document.querySelector('input[type="color"]');

    // Reset color picker to its default value on page load
    if (colorPicker) {
        colorPicker.value = colorPicker.defaultValue;
    }

    // Expose the functions globally for other scripts or inline event handlers to use
    window.togglePortfolioEditMode = togglePortfolioEditMode;
    window.savePortfolio = savePortfolio;
});
