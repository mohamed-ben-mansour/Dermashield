const lightModeToggle = document.getElementById('light-mode-toggle');
  lightModeToggle.addEventListener('click', () => {
    document.body.classList.toggle('light-mode');
    
    // Optional: Change button text based on mode
    if (document.body.classList.contains('light-mode')) {
      lightModeToggle.textContent = 'Dark Mode';
    } else {
      lightModeToggle.textContent = 'Light Mode';
    }
  });