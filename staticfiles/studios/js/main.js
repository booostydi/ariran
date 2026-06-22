// Sticky Navigation
const stickyNav = document.getElementById('stickyNav');
const hero = document.getElementById('hero');

if (stickyNav && hero) {
    window.addEventListener('scroll', () => {
        const heroBottom = hero.offsetTop + hero.offsetHeight;
        if (window.scrollY > heroBottom - 100) {
            stickyNav.classList.add('visible');
        } else {
            stickyNav.classList.remove('visible');
        }
    });
}

// Fade-in animation
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

console.log('Arirang Studio Management System loaded');

// Fallback: if IntersectionObserver is not supported, reveal fade-in elements
if (!('IntersectionObserver' in window)) {
    document.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible'));
} else {
    // Also reveal any fade-in elements that are already in the viewport on load
    window.addEventListener('load', () => {
        document.querySelectorAll('.fade-in').forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) el.classList.add('visible');
        });
    });
}