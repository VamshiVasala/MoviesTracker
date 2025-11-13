document.addEventListener("DOMContentLoaded", () => {
const searchInput = document.getElementById('searchInput');
  const movieCards = document.querySelectorAll('.movie-card');

  searchInput.addEventListener('keyup', () => {
    const query = searchInput.value.toLowerCase();

    movieCards.forEach(card => {
      const title = card.querySelector('h3').textContent.toLowerCase();
      const year = card.querySelector('p').textContent.toLowerCase();

      // show/hide movie based on title or year
      if (title.includes(query) || year.includes(query)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });
});