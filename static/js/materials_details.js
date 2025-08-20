

document.addEventListener('DOMContentLoaded', function () {
  const menuBtn = document.getElementById('menuBtn');
  const sidebar = document.getElementById('sidebar');
  const contentOverlay = document.getElementById('contentOverlay');
  const darkModeToggle = document.querySelector('.dark-mode-toggle');
  const htmlElement = document.documentElement;

  // Function to toggle the sidebar
  function toggleSidebar() {
    sidebar.classList.toggle('active');
    contentOverlay.classList.toggle('active');
  }

  // Toggle sidebar on menu button click
  menuBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleSidebar();
  });

  // Close sidebar when clicking on a link inside it
  const sidebarLinks = document.querySelectorAll('.sidebar a');
  sidebarLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (sidebar.classList.contains('active')) {
        toggleSidebar();
      }
    });
  });

  // Close sidebar when clicking on the overlay
  contentOverlay.addEventListener('click', () => {
    if (sidebar.classList.contains('active')) {
      toggleSidebar();
    }
  });

  // Dark Mode Toggle Functionality
  darkModeToggle.addEventListener('click', () => {
    const isDark = htmlElement.getAttribute('data-theme') === 'dark';
    if (isDark) {
      htmlElement.removeAttribute('data-theme');
      localStorage.setItem('theme', 'light');
    } else {
      htmlElement.setAttribute('data-theme', 'dark');
      localStorage.setItem('theme', 'dark');
    }
  });

  // Check for saved theme preference
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme === 'dark') {
    htmlElement.setAttribute('data-theme', 'dark');
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    // If no preference saved, check system preference
    htmlElement.setAttribute('data-theme', 'dark');
  }
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