document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggle-btn');
    const mainContent = document.getElementById('dashboard-content');

    // Function to handle sidebar collapse/expand based on screen width
    function handleScreenResize() {
        if (window.innerWidth < 768) {
            sidebar.classList.add('collapsed');
            mainContent.classList.add('collapsed');
            toggleBtn.querySelector('i').classList.remove('fa-arrow-left');
            toggleBtn.querySelector('i').classList.add('fa-arrow-right');
        } else {
            sidebar.classList.remove('collapsed');
            mainContent.classList.remove('collapsed');
            toggleBtn.querySelector('i').classList.remove('fa-arrow-right');
            toggleBtn.querySelector('i').classList.add('fa-arrow-left');
        }
    }

    // Run the function on page load and screen resize
    handleScreenResize();
    window.addEventListener('resize', handleScreenResize);

    // Toggle button click event
    toggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
        mainContent.classList.toggle('collapsed');
        toggleBtn.querySelector('i').classList.toggle('fa-arrow-left');
        toggleBtn.querySelector('i').classList.toggle('fa-arrow-right');
    });
});

