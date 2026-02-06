document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        
        const linkPath = link.getAttribute('href');
        
        if (currentPath === linkPath || (linkPath !== '#' && currentPath.startsWith(linkPath) && linkPath !== '/')) {
            link.classList.add('active');
        }
    });
});