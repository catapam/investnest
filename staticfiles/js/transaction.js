/**
 * Updates the hidden fields 'actionHidden' and 'typeHidden' based on the switch states.
 */
function updateHiddenFields() {
    var actionSwitch = document.getElementById('actionSwitch');
    var typeSwitch = document.getElementById('typeSwitch');
    var actionHidden = document.getElementById('actionHidden');
    var typeHidden = document.getElementById('typeHidden');

    // Update the hidden field values based on switch states
    if (actionSwitch.checked) {
        actionHidden.value = 'sell';  // Set to 'sell' if the action switch is checked
    } else {
        actionHidden.value = 'buy';   // Set to 'buy' if the action switch is unchecked
    }

    if (typeSwitch.checked) {
        typeHidden.value = 'short';   // Set to 'short' if the type switch is checked
    } else {
        typeHidden.value = 'long';    // Set to 'long' if the type switch is unchecked
    }
}

/**
 * Toggles visibility of the new asset name field based on the selected asset choice.
 */
function toggleAssetFields() {
    var assetChoiceField = document.getElementById("id_asset_choice");
    var divAssetChoiceField = document.getElementById("div_id_asset_choice");
    var divAssetNameField = document.getElementById("div_id_new_asset_name");
    var newAssetNameField = document.getElementById("id_new_asset_name");

    // Show or hide fields based on the value of the asset choice
    if (assetChoiceField.value === "new") {
        newAssetNameField.style.display = "block";   // Show new asset name input
        divAssetNameField.style.display = "block";   // Show div containing new asset name input
        divAssetChoiceField.style.display = "none";  // Hide asset choice field
    } else {
        newAssetNameField.style.display = "none";    // Hide new asset name input
        divAssetNameField.style.display = "none";    // Hide div containing new asset name input
        divAssetChoiceField.style.display = "block"; // Show asset choice field
    }
}

/**
 * Initializes the form based on the initial state of the asset choice and switch elements.
 */
function initializeForm() {
    // Initialize visibility based on current selection in asset choice field
    toggleAssetFields();

    // Ensure that the hidden fields reflect the initial switch states
    updateHiddenFields();
}

/**
 * Sets up event listeners for the asset choice field and switches.
 */
function setupEventListeners() {
    var assetChoiceField = document.getElementById("id_asset_choice");
    var actionSwitch = document.getElementById('actionSwitch');
    var typeSwitch = document.getElementById('typeSwitch');

    // Toggle asset fields when the asset choice changes
    assetChoiceField.addEventListener("change", toggleAssetFields);

    // Update hidden fields when switches are toggled
    actionSwitch.addEventListener('change', updateHiddenFields);
    typeSwitch.addEventListener('change', updateHiddenFields);

    // Ensure hidden fields are set correctly before form submission
    document.getElementById('transactionForm').addEventListener('submit', updateHiddenFields);
}

// DOMContentLoaded event listener to initialize the form and setup event listeners
document.addEventListener('DOMContentLoaded', function () {
    initializeForm();
    setupEventListeners();
});
