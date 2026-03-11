// Pelican Classificados — main.js
document.addEventListener('DOMContentLoaded', () => {
  // Prevent category/date links from triggering card link
  document.querySelectorAll('.card-link .card-category').forEach(el => {
    el.addEventListener('click', e => e.stopPropagation());
  });
  document.querySelectorAll('.card-link .card-location').forEach(el => {
    el.addEventListener('click', e => e.stopPropagation());
  });
  document.querySelectorAll('.card-link .card-date-link').forEach(el => {
    el.addEventListener('click', e => e.stopPropagation());
  });
});