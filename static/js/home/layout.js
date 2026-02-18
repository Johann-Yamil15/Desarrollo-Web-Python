document.addEventListener('DOMContentLoaded', function () {
    const currentPath = window.location.pathname;

    const navLinks = document.querySelectorAll('.nav-link');
    const btnToggle = document.getElementById('btnToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');

    if (btnToggle && sidebar && overlay) {
        btnToggle.addEventListener('click', () => {
            sidebar.classList.add('active');
            overlay.classList.add('active');
        });

        overlay.addEventListener('click', () => {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        });
    }

    navLinks.forEach(link => {
        link.classList.remove('active');

        const linkPath = link.getAttribute('href');

        if (currentPath === linkPath || (linkPath !== '#' && currentPath.startsWith(linkPath) && linkPath !== '/')) {
            link.classList.add('active');
        }
    });
});