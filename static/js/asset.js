document.addEventListener('DOMContentLoaded', function() {

    function toggleEditMode(transactionId, editMode = true) {
        const row = document.getElementById(`transaction-${transactionId}`);
        const displayModeElements = row.querySelectorAll('.display-mode');
        const editModeElements = row.querySelectorAll('.edit-mode');
        const editButton = row.querySelector('.btn-edit');
        const deleteButton = row.querySelector('.btn-delete');
        const saveButton = row.querySelector('.btn-save');
        const cancelButton = row.querySelector('.btn-cancel');

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

    function saveTransaction(transactionId) {
        const row = document.getElementById(`transaction-${transactionId}`);
        const type = row.querySelector('select[name="type"]').value;
        const action = row.querySelector('select[name="action"]').value;
        const quantity = row.querySelector('input[name="quantity"]').value;
        const price = row.querySelector('input[name="price"]').value;
        const date = row.querySelector('input[name="date"]').value;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/portfolio/transaction/update/${transactionId}/`, {
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
                location.reload();  // Reload the page on success
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

    function deleteTransaction(transactionId) {
        if (!confirm('Are you sure you want to delete this transaction?')) return;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/portfolio/transaction/delete/${transactionId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => {
            if (response.ok) {
                location.reload();  // Reload the page on successful deletion
            } else {
                return response.json().then(err => { throw err; });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to delete the transaction. Please try again.');
        });
    }

    function toggleAssetEditMode(editMode) {
        const assetNameDisplay = document.getElementById('asset-name-display');
        const assetNameForm = document.getElementById('asset-name-form');
        const editAssetNameBtn = document.getElementById('edit-asset-name-btn');
        const deleteAssetBtn = document.getElementById('delete-asset-btn');

        if (editMode) {
            assetNameDisplay.style.display = 'none';
            assetNameForm.style.display = 'block';
            editAssetNameBtn.style.display = 'none';
            deleteAssetBtn.style.display = 'none';
        } else {
            assetNameDisplay.style.display = 'block';
            assetNameForm.style.display = 'none';
            editAssetNameBtn.style.display = 'inline-block';
            deleteAssetBtn.style.display = 'inline-block';
        }
    }

    function saveAssetName(assetId, portfolioId) {
        const assetNameInput = document.querySelector('#asset-name-form input[name="name"]');
        const newName = assetNameInput.value.trim();
    
        if (newName === '') {
            alert('Asset name cannot be empty.');
            return;
        }
    
        const formData = new FormData();
        formData.append('name', newName);
    
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        formData.append('csrfmiddlewaretoken', csrfToken);
    
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
                location.reload();  // Reload the page on success
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

    function deleteAsset(assetId, portfolioId) {
        if (!confirm('Are you sure you want to delete this asset? Be aware that all transactions for this asset will also be deleted if you proceed')) return;
    
        let csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        if (!csrfTokenElement) {
            csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        } else{
            csrfToken = csrfTokenElement.value
        }

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
                // Handle other response statuses
                return response.text().then(text => { throw new Error(text); });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to delete the asset. Please try again.');
        });
    }
     
    window.toggleEditMode = toggleEditMode;
    window.saveTransaction = saveTransaction;
    window.deleteTransaction = deleteTransaction;
    window.toggleAssetEditMode = toggleAssetEditMode;
    window.saveAssetName = saveAssetName;
    window.deleteAsset = deleteAsset;
});
