// Custom sidebar toggle for Django admin (Jazzmin)
document.addEventListener('DOMContentLoaded', function() {
    var body = document.body;
    var sidebarToggle = document.querySelector('.sidebar-toggle, .nav-link[data-widget="pushmenu"]');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function(e) {
            e.preventDefault();
            body.classList.toggle('sidebar-collapse');
        });
    }
    // Also close sidebar on overlay click (for mobile)
    var overlay = document.querySelector('.sidebar-overlay');
    if (overlay) {
        overlay.addEventListener('click', function() {
            body.classList.add('sidebar-collapse');
        });
    }
});
