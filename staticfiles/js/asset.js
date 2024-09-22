/**
 * Toggles between the display and edit mode for a transaction row.
 * @param {number} transactionId - The ID of the transaction to toggle.
 * @param {boolean} editMode - Set to true to switch to edit mode, false to switch to display mode.
 */
function toggleEditMode(transactionId, editMode = true) {
    var row = document.getElementById(`transaction-${transactionId}`);
    var displayModeElements = row.querySelectorAll('.display-mode');
    var editModeElements = row.querySelectorAll('.edit-mode');
    var editButton = row.querySelector('.btn-edit');
    var deleteButton = row.querySelector('.btn-delete');
    var saveButton = row.querySelector('.btn-save');
    var cancelButton = row.querySelector('.btn-cancel');

    // Toggle between edit and display modes
    if (editMode) {
        displayModeElements.forEach(element => element.style.display = 'none');
        editModeElements.forEach(element => element.style.display = 'block');
        editButton.style.display = 'none';
        deleteButton.style.display = 'none';
        saveButton.style.display = 'inline-block';
        cancelButton.style.display = 'inline-block';
    } else {
        displayModeElements.forEach(element => element.style.display = 'block');
        editModeElements.forEach(element => element.style.display = 'none');
        editButton.style.display = 'inline-block';
        deleteButton.style.display = 'inline-block';
        saveButton.style.display = 'none';
        cancelButton.style.display = 'none';
    }
}

/**
 * Saves the transaction by sending a POST request to update it.
 * @param {number} portfolioId - The ID of the portfolio the asset belongs to.
 * @param {number} assetId - The ID of the asset the transaction belongs to.
 * @param {number} transactionId - The ID of the transaction to save.
 */
function saveTransaction(portfolioId, assetId, transactionId) {
    var row = document.getElementById(`transaction-${transactionId}`);
    var type = row.querySelector('select[name="type"]').value;
    var action = row.querySelector('select[name="action"]').value;
    var quantity = row.querySelector('input[name="quantity"]').value;
    var price = row.querySelector('input[name="price"]').value;
    var date = row.querySelector('input[name="date"]').value;

    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Send a POST request to update the transaction
    fetch(`/portfolio/${portfolioId}/asset/${assetId}/transaction/${transactionId}/update/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        body: JSON.stringify({
            'type': type,
            'action': action,
            'quantity': quantity,
            'price': price,
            'date': date
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
            location.reload();  // Reload page on success
        } else {
            console.error('Error:', data.errors);
            alert('Failed to save the transaction. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while saving the transaction. Please try again.');
    });
}

/**
 * Toggles between the display and edit mode for the asset name.
 * @param {boolean} editMode - Set to true to enable edit mode, false to return to display mode.
 */
function toggleAssetEditMode(editMode) {
    var assetNameDisplay = document.getElementById('asset-name-display');
    var assetNameForm = document.getElementById('asset-name-form');
    var editAssetNameBtn = document.getElementById('edit-asset-name-btn');
    var deleteAssetBtn = document.getElementById('delete-asset-btn');
    var cancelAssetBtn = document.getElementById('asset-cancel-btn');
    var saveAssetBtn = document.getElementById('asset-save-btn');
    var allAssetBtn = document.getElementById('asset-all-btn');

    // Toggle between edit and display modes for asset name
    if (editMode) {
        assetNameDisplay.style.display = 'none';
        assetNameForm.style.display = 'flex';
        allAssetBtn.style.display = 'none';
        editAssetNameBtn.style.display = 'none';
        deleteAssetBtn.style.display = 'none';
        cancelAssetBtn.style.display = 'inline-block';
        saveAssetBtn.style.display = 'inline-block';
    } else {
        assetNameDisplay.style.display = 'inline-block';
        assetNameForm.style.display = 'none';
        allAssetBtn.style.display = 'inline-block';
        editAssetNameBtn.style.display = 'inline-block';
        deleteAssetBtn.style.display = 'inline-block';
        cancelAssetBtn.style.display = 'none';
        saveAssetBtn.style.display = 'none';
    }
}

/**
 * Saves the updated asset name by sending a POST request.
 * @param {number} assetId - The ID of the asset to update.
 * @param {number} portfolioId - The ID of the portfolio the asset belongs to.
 */
function saveAssetName(assetId, portfolioId) {
    var assetNameInput = document.querySelector('#asset-name-form input[name="name"]');
    var newName = assetNameInput.value.trim();

    if (newName === '') {
        alert('Asset name cannot be empty.');
        return;
    }

    var formData = new FormData();
    formData.append('name', newName);

    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    formData.append('csrfmiddlewaretoken', csrfToken);

    // Send a POST request to update the asset name
    fetch(`/portfolio/${portfolioId}/asset/${assetId}/edit/`, {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            return response.json().then(err => { throw err; });
        }
    })
    .then(data => {
        if (data.status === 'success') {
            location.reload();  // Reload page on success
        } else {
            console.error('Error:', data.errors);
            alert('Failed to save the asset name: ' + data.errors.name);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while saving the asset name. Please try again.');
    });
}

/**
 * Deletes an asset and its transactions after confirmation.
 * @param {number} assetId - The ID of the asset to delete.
 * @param {number} portfolioId - The ID of the portfolio the asset belongs to.
 */
function deleteAsset(assetId, portfolioId) {
    if (!confirm('Are you sure you want to delete this asset? All transactions will also be deleted.')) return;

    var csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    var csrfToken = csrfTokenElement ? csrfTokenElement.value : document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Send a DELETE request to delete the asset
    fetch(`/portfolio/${portfolioId}/asset/${assetId}/delete/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken,
        },
    })
    .then(response => {
        if (response.ok) {
            window.location.href = `/portfolio/${portfolioId}/`;  // Redirect to portfolio detail page
        } else {
            return response.text().then(text => { throw new Error(text); });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to delete the asset. Please try again.');
    });
}

/**
 * Initializes the functions after the DOM content has fully loaded.
 */
document.addEventListener('DOMContentLoaded', function() {
    window.toggleEditMode = toggleEditMode;
    window.saveTransaction = saveTransaction;
    window.toggleAssetEditMode = toggleAssetEditMode;
    window.saveAssetName = saveAssetName;
    window.deleteAsset = deleteAsset;
});
