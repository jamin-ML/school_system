// Toggle sidebar on mobile
  document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('toggleSidebar');
    const sidebar = document.querySelector('aside');

    toggleButton.addEventListener('click', function () {
      sidebar.classList.toggle('hidden');
    });

    // Back to Top button
    const backToTopBtn = document.getElementById('backToTopBtn');

    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        backToTopBtn.classList.remove('hidden');
      } else {
        backToTopBtn.classList.add('hidden');
      }
    });

    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  });
  // Toggle sidebar on mobile
  document.getElementById('mobileMenuButton').addEventListener('click', function() {
    document.getElementById('sidebar').classList.toggle('translate-x-0');
  });
