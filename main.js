// Add smooth scrolling and other animations
document.addEventListener('DOMContentLoaded', function() {
    // Animate form submission
    const form = document.querySelector('.search-form');
    if (form) {
        form.addEventListener('submit', function() {
            form.style.opacity = '0.5';
            form.style.transform = 'scale(0.95)';
        });
    }
}); 