document.addEventListener('DOMContentLoaded', function() {

    var actionSwitch = document.getElementById('actionSwitch');
    var typeSwitch = document.getElementById('typeSwitch');
    var actionHidden = document.getElementById('actionHidden');
    var typeHidden = document.getElementById('typeHidden');

    var assetChoiceField = document.getElementById("id_asset_choice");
    var divAssetChoiceField = document.getElementById("div_id_asset_choice");
    var divAssetNameField = document.getElementById("div_id_new_asset_name");
    var newAssetNameField = document.getElementById("id_new_asset_name");

    assetChoiceField.addEventListener("change", function () {
        if (assetChoiceField.value === "new") {
            newAssetNameField.style.display = "block";
            divAssetNameField.style.display = "block";
            divAssetChoiceField.style.display = "none";
        } else {
            newAssetNameField.style.display = "none";
            divAssetNameField.style.display = "none";
            divAssetChoiceField.style.display = "block";
        }
    });

    // Initialize visibility based on current selection
    if (assetChoiceField.value === "new") {
        newAssetNameField.style.display = "block";
        divAssetNameField.style.display = "block";
        divAssetChoiceField.style.display = "none";
    } else {
        newAssetNameField.style.display = "none";
        divAssetNameField.style.display = "none";
        divAssetChoiceField.style.display = "block";
    }

    // Ensure that the hidden fields reflect the initial switch states
    updateHiddenFields();

    actionSwitch.addEventListener('change', function() {
        updateHiddenFields();
    });

    typeSwitch.addEventListener('change', function() {
        updateHiddenFields();
    });

    function updateHiddenFields() {
        if (actionSwitch.checked) {
            actionHidden.value = 'sell';
        } else {
            actionHidden.value = 'buy';
        }

        if (typeSwitch.checked) {
            typeHidden.value = 'short';
        } else {
            typeHidden.value = 'long';
        }
    }

    // Ensure hidden fields are set correctly before form submission
    document.getElementById('transactionForm').addEventListener('submit', function() {
        updateHiddenFields();
    });

});
