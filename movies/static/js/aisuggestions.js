document.addEventListener("DOMContentLoaded", () => {
    const currentPage = 1;
    let api = `/api/recommended-movies/?page=${currentPage}`;

    const container = document.getElementById('movieContainer');
    function loadMovies() {
        if (!api) {
            return;
        }
        fetch(api)
            .then(response => response.json())
            .then(data => {
                console.log("Wikipedia Summary:", data.results);
                if (data.next != null) {
                    const s = data.next;
                    let t = s.slice(s.length - 1, s.length);
                    api = api.slice(0, -1) + t;
                }
                else {
                    api = null;
                }
                data.results.forEach(movie => {

                    const movieCard = document.createElement("div");
                    movieCard.classList.add("movie-card");

                    const title = document.createElement("h3")
                    title.classList.add("title")
                    title.textContent = `${movie.title}`;
                    movieCard.appendChild(title);

                    const year = document.createElement("h3")
                    year.classList.add("title")
                    year.textContent = `${movie.year_of_release}`;
                    movieCard.appendChild(year);

                    const img = document.createElement("img");
                    if (movie.poster_url) {
                        img.src = movie.poster_url;
                        // img.alt = movie.title;
                        movieCard.appendChild(img);
                    }

                    const synopsis = document.createElement('p');
                    synopsis.textContent = movie.short_synopsis; // display movie title
                    movieCard.appendChild(synopsis);

                    container.appendChild(movieCard);


                });

            });
    }
    loadMovies();

    container.addEventListener('scroll', function () {
        if (container.scrollTop + container.clientHeight >= container.scrollHeight - 5) {
            loadMovies(); // load next page
        }
    });

});