
document.addEventListener("DOMContentLoaded", () => {
    let globaluse = [];
    let reviewList = [];
    let likedMap = new Map();
    let dislikedMap = new Map();
    fetch('/get_movies_api/')
        .then(response => response.json())
        .then(data => {
            const movies = data.movies;
            const reviews = data.reviews;
            const reaction = data.reactions;
            counts = data.countserializer;
            for (let i = 0; i < counts.length; i++) {
                for (let j = 0; j < counts[i].likedMovies.length; j++) {
                    let movieId = counts[i].likedMovies[j];
                    if (likedMap.has(movieId)) {
                        likedMap.set(movieId, likedMap.get(movieId) + 1);
                    }
                    else {
                        likedMap.set(movieId, 1);
                    }
                }
                for (let k = 0; k < counts[i].dislikedMovies.length; k++) {
                    let movieId = counts[i].dislikedMovies[k];
                    if (dislikedMap.has(movieId)) {
                        dislikedMap.set(movieId, dislikedMap.get(movieId) + 1);
                    }
                    else {
                        dislikedMap.set(movieId, 1);
                    }
                }
            }
            reactions = reaction;
            const moviesExplore = data.moviesExplore;
            displayMovies(data.recommendedMovies, reviews);
            globaluse = moviesExplore;
            reviewList = reviews;
            const analysisUrl = data.analysisUrl;
            selectcategories();
        });


    function selectcategories() {
        let genres = []; // reset before adding
        let cast = [];   // reset before adding

        for (let i = 0; i < globaluse.length; i++) {
            genres.push(globaluse[i].genres); // spread to avoid nested list
            cast.push(globaluse[i].cast);
        }
        let genreList = genres.flatMap(item => item.split(","));
        let castList = cast.flatMap(item => item.split(","));
        let cleanedDataGenre = [];
        let cleanedDataCast = [];
        console.log("Raw Genres:", genreList);
        console.log("Raw Cast:", castList);
        for (let i = 0; i < genreList.length; i++) {
            genreList[i] = genreList[i].trim();
            let lists = genreList[i].split(" ");
            for (let j = 0; j < lists.length; j++) {
                cleanedDataGenre.push(lists[j]);
            }
        }
        console.log("Cleaned Genres:", cleanedDataGenre);
        genres = [...new Set(cleanedDataGenre)];
        cast = [...new Set(castList.map(item => item.trim()))];
        console.log("Genres:", genres);
        console.log("Cast:", cast);
        const genreSelect = document.getElementById("genreContainer");
        const castSelect = document.getElementById("castContainer");
        genres.forEach(g => genreSelect.innerHTML += `<label class='pill'><input type="checkbox" value="${g}" class="genreCheck">${g}</input></label>`);
        cast.forEach(c => castSelect.innerHTML += `<label class='pill'><input type="checkbox" value="${c}" class="castCheck">${c}</input></label>`);

        document.querySelectorAll(".genreCheck, .castCheck")
            .forEach(cb => cb.addEventListener("change", filterMovies));
    }
    function filterMovies() {
        const genreSelect = document.getElementById("genreContainer");
        const castSelect = document.getElementById("castContainer");
        let selectedGenreValues = [];
        let selectedCastValues = [];
        for (let i = 0; i < genreSelect.children.length; i++) {
            if (genreSelect.children[i].childNodes[0].checked) {
                selectedGenreValues.push(genreSelect.children[i].childNodes[0].defaultValue);
            }
        }
        for (let i = 0; i < castSelect.children.length; i++) {
            if (castSelect.children[i].childNodes[0].checked) {
                selectedCastValues.push(castSelect.children[i].childNodes[0].defaultValue);
            }
        }
        if (selectedGenreValues.length === 0 && selectedCastValues.length === 0) {
            displayMovies(globaluse, reviewList);
            return;
        }
        let filteredMovies = globaluse;
        let movies = [];
        filteredMovies.forEach(movie => {
            let flag = true;
            const genres = movie.genres.split(",").map(g => g.trim());
            const Genre = [];
            for (let j = 0; j < genres.length; j++) {
                let string = genres[j].split(" ");
                for (let k = 0; k < string.length; k++) {
                    Genre.push(string[k]);
                }
            }
            const casts = movie.cast.split(",").map(c => c.trim());
            for (let m = 0; m < selectedGenreValues.length; m++) {
                if (Genre.includes(selectedGenreValues[m])) {
                    movies.push(movie);
                    flag = false;
                    break;
                }
            }
            if (flag) {
                for (let m = 0; m < selectedCastValues.length; m++) {
                    if (casts.includes(selectedCastValues[m])) {
                        movies.push(movie);
                        break;
                    }
                }
            }
        })
        displayMovies(movies, reviewList);


    }


    function displayMovies(moviess, reviews) {
        const container = document.getElementById("movies-container");
        container.innerHTML = "";
        moviess.forEach(movie => {
            const movieReviewed = reviews.filter(rev => rev.movie === movie.id);
            if (movieReviewed.length > 0) {
                const movieDiv = document.createElement("div");
                movieDiv.classList.add("movie");

                const title = document.createElement("h2");
                movieDiv.classList.add("title");
                title.textContent = `${movie.title} (${movie.year})`;
                movieDiv.appendChild(title);

                const forAnalysis = document.createElement("a");
                forAnalysis.href = analysisUrl;

                const img = document.createElement("img");
                img.src = movie.image_url;
                img.alt = movie.title;
                img.setAttribute("data-id", movie.id);

                forAnalysis.appendChild(img);
                movieDiv.appendChild(forAnalysis);

                img.addEventListener("click", (event) => {
                    const movieID = event.target.getAttribute("data-id");
                    localStorage.setItem("reviewList", JSON.stringify(movieID));
                });



                const ratingDiv = document.createElement("div");
                ratingDiv.classList.add("stars");
                let fullStars = (movieReviewed[0].stars);
                for (let i = 1; i <= 5; i++) {
                    const star = document.createElement("span");
                    star.classList.add("star");
                    star.innerHTML = i <= fullStars ? "&#9733;" : "&#9734;";
                    ratingDiv.appendChild(star);
                }
                movieDiv.appendChild(ratingDiv);

                const opinion = document.createElement("p");
                opinion.textContent = movieReviewed[0].opinion;
                movieDiv.appendChild(opinion);

                const reactionContent = document.createElement("div");
                reactionContent.classList.add("reaction-content");

                const likeWrapper = document.createElement("div");
                likeWrapper.classList.add("like-wrapper");

                const likes = document.createElement("i");
                likes.classList.add("fa-regular", "fa-thumbs-up");
                likes.setAttribute("data-id", movie.id);

                const likesCount = document.createElement("span");
                likesCount.classList.add("like-count");
                likesCount.innerText = likedMap?.get(movie.id) || 0;

                likeWrapper.appendChild(likes);
                likeWrapper.appendChild(likesCount);

                const dislikeWrapper = document.createElement("div");
                dislikeWrapper.classList.add("dislike-wrapper");

                const dislikes = document.createElement("i");
                dislikes.classList.add("fa-regular", "fa-thumbs-down");
                dislikes.setAttribute("data-id", movie.id);

                const dislikeCount = document.createElement("span");
                dislikeCount.classList.add("dislike-count");
                dislikeCount.innerText = dislikedMap?.get(movie.id) || 0;

                dislikeWrapper.appendChild(dislikes);
                dislikeWrapper.appendChild(dislikeCount);

                reactionContent.appendChild(likeWrapper);
                reactionContent.appendChild(dislikeWrapper);

                movieDiv.appendChild(reactionContent);

                for (let i = 0; i < reactions.length; i++) {
                    if (reactions[i].likedMovies.includes(movie.id)) {
                        likes.classList.add("fa-solid");
                        dislikes.classList.remove("fa-solid");
                    }
                    if (reactions[i].dislikedMovies.includes(movie.id)) {
                        dislikes.classList.add("fa-solid");
                        likes.classList.remove("fa-solid");
                    }
                }

                likes.addEventListener("click", () => {
                    const MovieID = likes.attributes["data-id"].nodeValue;
                    let currCount = parseInt(likes.nextElementSibling.childNodes[0].nodeValue);
                    if (likes.classList.contains("fa-solid")) {
                        likes.nextElementSibling.childNodes[0].nodeValue=currCount - 1;
                    }
                    else {
                        likes.nextElementSibling.childNodes[0].nodeValue = currCount + 1;
                    }
                    if (dislikes.classList.contains("fa-solid")) {
                        let currDislikeCount = parseInt(dislikes.nextElementSibling.childNodes[0].nodeValue);
                        dislikes.nextElementSibling.childNodes[0].nodeValue = currDislikeCount - 1;
                    }
                    likes.classList.toggle("fa-solid"); // highlight dislike
                    dislikes.classList.remove("fa-solid");

                    fetch(`/reaction/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": getCookie("csrftoken"), // 🔒 Required for Django
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            id: MovieID,
                            flag: true,
                        })
                    })
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);
                            if (data.status === "success") {
                                console.log("Reaction recorded");
                            }
                        })
                        .catch(error => console.error("Error:", error));
                });

                dislikes.addEventListener("click", () => {
                    const MovieID = dislikes.attributes["data-id"].nodeValue;
                    let currCount = parseInt(dislikes.nextElementSibling.childNodes[0].nodeValue);
                    if (dislikes.classList.contains("fa-solid")) {
                        dislikes.nextElementSibling.childNodes[0].nodeValue = currCount - 1;
                    }
                    else {
                        dislikes.nextElementSibling.childNodes[0].nodeValue = currCount + 1;
                    }
                    if (likes.classList.contains("fa-solid")) {
                        let currLikeCount = parseInt(likes.nextElementSibling.childNodes[0].nodeValue);
                        likes.nextElementSibling.childNodes[0].nodeValue= currLikeCount - 1;
                    }
                    dislikes.classList.toggle("fa-solid"); // highlight dislike
                    likes.classList.remove("fa-solid");
                    fetch(`/reaction/`, {
                        method: "POST",
                        headers: {
                            "X-CSRFToken": getCookie("csrftoken"), // 🔒 Required for Django
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            id: MovieID,
                            flag: false,
                        })
                    })
                        .then(response => response.json())
                        .then(data => {
                            console.log(data);
                            if (data.status === "success") {
                                console.log("Reaction recorded");
                            }
                        })
                        .catch(error => console.error("Error:", error));
                });
                container.appendChild(movieDiv);
            }

        });
    }



    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

});

