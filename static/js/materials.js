document.addEventListener('DOMContentLoaded', function () {
    // Initialize AOS animations
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-in-out',
            once: true
        });
    }

    // Dark Mode Toggle Functionality
    const darkModeToggle = document.querySelector('.dark-mode-toggle');
    const htmlElement = document.documentElement;
    const darkIcon = document.querySelector('.dark-icon');
    const lightIcon = document.querySelector('.light-icon');

    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            const isDark = htmlElement.getAttribute('data-theme') === 'dark';
            console.log('Toggling theme. Current:', isDark ? 'dark' : 'light');
            if (isDark) {
                htmlElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
                darkIcon.classList.remove('hidden');
                lightIcon.classList.add('hidden');
                console.log('Switched to light mode');
            } else {
                htmlElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
                darkIcon.classList.add('hidden');
                lightIcon.classList.remove('hidden');
                console.log('Switched to dark mode');
            }
        });
    } else {
        console.error('Dark mode toggle element not found');
    }

    // Check for saved theme preference or system preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        htmlElement.setAttribute('data-theme', savedTheme);
        console.log('Applying saved theme:', savedTheme);
        if (savedTheme === 'dark') {
            darkIcon.classList.add('hidden');
            lightIcon.classList.remove('hidden');
        } else {
            darkIcon.classList.remove('hidden');
            lightIcon.classList.add('hidden');
        }
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        htmlElement.setAttribute('data-theme', 'dark');
        darkIcon.classList.add('hidden');
        lightIcon.classList.remove('hidden');
        console.log('Applied system preference: dark');
    } else {
        htmlElement.setAttribute('data-theme', 'light');
        darkIcon.classList.remove('hidden');
        lightIcon.classList.add('hidden');
        console.log('Applied default: light');
    }

    // Testimonial slider functionality
    const slides = document.querySelectorAll('.testimonial-slide');
    const dots = document.querySelectorAll('.slider-dot');

    dots.forEach(dot => {
        dot.addEventListener('click', function () {
            const slideIndex = this.getAttribute('data-slide');
            slides.forEach(slide => slide.classList.remove('active'));
            dots.forEach(dot => dot.classList.remove('active'));
            slides[slideIndex].classList.add('active');
            this.classList.add('active');
        });
    });

    // Mobile menu functionality
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mainNav = document.getElementById('mainNav');

    if (mobileMenuBtn && mainNav) {
        mobileMenuBtn.addEventListener('click', function () {
            mainNav.classList.toggle('active');
        });
    }

    // Smooth scroll for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
});

// Add scroll progress indicator
const progressBar = document.createElement('div');
progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    width: 0%;
    height: 3px;
    background: linear-gradient(90deg, var(--accent-color), #22c55e);
    z-index: 10000;
    transition: width 0.1s ease;
`;
document.body.appendChild(progressBar);

window.addEventListener('scroll', function () {
    const scrolled = (window.pageYOffset / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
    progressBar.style.width = scrolled + '%';
});