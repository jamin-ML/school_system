// Initialize AOS (Animate On Scroll)
AOS.init({
    duration: 800,
    easing: 'ease-in-out',
    once: true
});

// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mainNav = document.getElementById('mainNav');
if (mobileMenuBtn && mainNav) {
    mobileMenuBtn.addEventListener('click', () => {
        mainNav.classList.toggle('active');
        mobileMenuBtn.innerHTML = mainNav.classList.contains('active') ? 
            '<i class="fas fa-times"></i>' : '<i class="fas fa-bars"></i>';
    });
}

// Dark Mode Toggle
const darkModeToggle = document.getElementById('darkModeToggle');
if (darkModeToggle) {
    // Check for saved user preference or use system preference
    if (localStorage.getItem('darkMode') === 'enabled' || 
        (!localStorage.getItem('darkMode') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.body.classList.add('dark-mode');
        darkModeToggle.checked = true;
    }
    darkModeToggle.addEventListener('change', () => {
        document.body.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', document.body.classList.contains('dark-mode') ? 'enabled' : 'disabled');
    });
}

// Testimonial Slider
const slides = document.querySelectorAll('.testimonial-slide');
const dots = document.querySelectorAll('.slider-dot');
let currentSlide = 0;

function showSlide(index) {
    slides.forEach(slide => slide.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));
    
    slides[index].classList.add('active');
    dots[index].classList.add('active');
    currentSlide = index;
}

if (dots.length && slides.length) {
    dots.forEach(dot => {
        dot.addEventListener('click', () => {
            showSlide(parseInt(dot.getAttribute('data-slide')));
        });
    });
    // Auto slide change
    setInterval(() => {
        currentSlide = (currentSlide + 1) % slides.length;
        showSlide(currentSlide);
    }, 5000);
}

// Language Switcher (placeholder functionality)
const languageSelect = document.getElementById('languageSelect');
if (languageSelect) {
    languageSelect.addEventListener('change', () => {
        // In a real implementation, this would change the language of the content
        alert(`Language changed to ${languageSelect.value === 'en' ? 'English' : 'Kiswahili'}. This is a demo - actual implementation would translate the content.`);
    });
}

// Floating chat button
const chatBtn = document.querySelector('.chat-btn');
if (chatBtn) {
    chatBtn.addEventListener('click', () => {
        alert("This would open a live chat interface with a teacher in a real implementation.");
    });
}

// Make footer visible on page load
window.addEventListener('DOMContentLoaded', () => {
    const footer = document.querySelector('footer');
    if (footer) {
        footer.classList.add('visible');
    }
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
            
            // Close mobile menu if open
            if (mainNav && mainNav.classList.contains('active')) {
                mainNav.classList.remove('active');
                if (mobileMenuBtn) mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
            }
        }
    });
});