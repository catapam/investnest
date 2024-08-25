document.addEventListener('DOMContentLoaded', function() {
    var colorPicker = document.querySelector('input[type="color"]');
    if (colorPicker) {
        colorPicker.value = colorPicker.defaultValue;
    }
});
