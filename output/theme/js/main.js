// Pelican Classificados — main.js
// Subtle newspaper interactions

document.addEventListener('DOMContentLoaded', () => {

  // Staggered card entrance animation
  const cards = document.querySelectorAll('.card');
  cards.forEach((card, i) => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(6px)';
    card.style.transition = `opacity 0.3s ease ${i * 0.04}s, transform 0.3s ease ${i * 0.04}s`;
    setTimeout(() => {
      card.style.opacity = '1';
      card.style.transform = 'translateY(0)';
    }, 30);
  });

  // Category links — prevent double navigation when clicking category inside card link
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
