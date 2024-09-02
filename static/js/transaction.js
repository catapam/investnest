document.addEventListener('DOMContentLoaded', function() {

    const actionSwitch = document.getElementById('actionSwitch');
    const typeSwitch = document.getElementById('typeSwitch');
    const actionHidden = document.getElementById('actionHidden');
    const typeHidden = document.getElementById('typeHidden');

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
