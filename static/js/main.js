// Small script to show a loading overlay when the form is submitted.
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('scrapeForm');
  const overlay = document.getElementById('loadingOverlay');
  if (!form || !overlay) return;

  form.addEventListener('submit', function () {
    // Show overlay immediately so user sees something while server works.
    overlay.classList.remove('d-none');
    // Prevent the overlay disappearing if the server redirects quickly.
    // The page will be replaced when the server responds.
  });
});
