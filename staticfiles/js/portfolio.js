document.addEventListener('DOMContentLoaded', function () {
    var colorPicker = document.querySelector('input[type="color"]');
    if (colorPicker) {
        colorPicker.value = colorPicker.defaultValue;
    }

    var assetChoiceField = document.getElementById("id_asset_choice");
    var divAssetChoiceField = document.getElementById("div_id_asset_choice");
    var newAssetNameField = document.getElementById("div_id_new_asset_name");

    assetChoiceField.addEventListener("change", function () {
        if (assetChoiceField.value === "new") {
            newAssetNameField.style.display = "block";
            divAssetChoiceField.style.display = "none";
        } else {
            newAssetNameField.style.display = "none";
            divAssetChoiceField.style.display = "block";
        }
    });

    // Initialize visibility based on current selection
    if (assetChoiceField.value === "new") {
        newAssetNameField.style.display = "block";
        divAssetChoiceField.style.display = "none";
    } else {
        newAssetNameField.style.display = "none";
        divAssetChoiceField.style.display = "block";
    }
});
