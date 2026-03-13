// chiicones — main.js

document.addEventListener('DOMContentLoaded', () => {

    // Marca o link de navegação ativo
    const currentPath = window.location.pathname;
    document.querySelectorAll('.site-nav__link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.style.color = 'var(--color-accent)';
        }
    });

    // Scroll suave para links internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', e => {
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

});
