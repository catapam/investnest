document.addEventListener('DOMContentLoaded', function () {
    var colorPicker = document.querySelector('input[type="color"]');
    if (colorPicker) {
        colorPicker.value = colorPicker.defaultValue;
    }

    function togglePortfolioEditMode(portfolioId, editMode = true) {
        var row = document.getElementById(`portfolio-header`);
        var displayModeElements = row.querySelectorAll('.display-mode');
        var editModeElements = row.querySelectorAll('.edit-mode');
        var editButton = row.querySelector('.btn-edit');
        var deleteButton = row.querySelector('.btn-delete');
        var saveButton = row.querySelector('.btn-save');
        var cancelButton = row.querySelector('.btn-cancel');
        var metricsButton = row.querySelector('.btn-metrics');

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

    function savePortfolio(portfolioId) {
        var row = document.getElementById(`portfolio-header`);
        var name = row.querySelector('input[name="name"]').value;
        var description = row.querySelector('input[name="description"]').value;
        var color = row.querySelector('input[name="color"]').value;
        var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/portfolio/${portfolioId}/edit/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
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
                location.reload(); 
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

    window.togglePortfolioEditMode = togglePortfolioEditMode;
    window.savePortfolio = savePortfolio;
});
