// const API_KEY = "03e29c09848ae231e6eebf5873e5b7fd";


document.addEventListener("DOMContentLoaded", () => {
API_KEY=TMDB_API_KEY;
const titleInput = document.getElementById("id_title");
const descInput = document.getElementById("id_description");
const yearInput = document.getElementById("id_year");
const imageInput = document.getElementById("id_image_url");
const suggestions = document.getElementById("suggestions");
const posterPreview = document.getElementById("posterPreview");
const genresInput = document.getElementById("id_genres");
const castInput = document.getElementById("id_cast");

// when typing in title
titleInput.addEventListener("input", async () => {
  const query = titleInput.value.trim();
  if (!query) {
    suggestions.innerHTML = "";
    return;
  }

  const res = await fetch(
    `https://api.themoviedb.org/3/search/multi?api_key=${API_KEY}&query=${encodeURIComponent(query)}`
  );
  const data = await res.json();
  const results = data.results.slice(0, 8);

  suggestions.innerHTML = results
    .map(
      m => `
        <li data-id="${m.id}" data-type="${m.media_type}">
          <img src="https://image.tmdb.org/t/p/w92${m.poster_path || m?.known_for?.[0]?.poster_path}" />
          <span>${m.title || m.name} (${m.release_date?.split('-')[0] || m.first_air_date?.split('-')[0] || m.known_for[0]?.release_date?.split('-')[0]})</span>
        </li>`
    )
    .join("");
});

// when selecting a movie
suggestions.addEventListener("click", async (e) => {
  const li = e.target.closest("li");
  if (!li) return;
  const movieId = li.dataset.id;
  const cinema_type = li.dataset.type;
  const detailsRes = await fetch(
    `https://api.themoviedb.org/3/${cinema_type}/${movieId}?api_key=${API_KEY}&append_to_response=credits`
  );
  const movie = await detailsRes.json();

  // fill Django fields
  titleInput.value = movie?.title || movie?.name; 
  descInput.value = movie.overview || "";
  yearInput.value = movie?.release_date?.split("-")[0] || movie?.first_air_date?.split('-')[0] || movie?.known_for[0]?.release_date?.split('-')[0];
  imageInput.value = "https://image.tmdb.org/t/p/w342" + (movie?.poster_path || movie?.known_for[0].poster_path);
  genresInput.value = movie.genres.map(g => g.name).join(", ");
  castInput.value = movie.credits.cast.slice(0, 5).map(c => c.name).join(", ");
  // image preview
  if (movie.poster_path) {
    posterPreview.src = "https://image.tmdb.org/t/p/w342" + (movie?.poster_path || movie?.known_for[0]?.poster_path);
    posterPreview.style.display = "block";
  }
  suggestions.innerHTML = "";
});});