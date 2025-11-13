document.addEventListener("DOMContentLoaded", () => {
  fetch('/get_data/')
    .then(response => response.json())
    .then(data => {
      const movies = data.movies;
      const reviews = data.reviews;
      const container = document.getElementById("movies-container");
      movies.forEach(movie => {
        const movieReviews = reviews.filter(review => review.id === movie.reviews);

        const movieDiv = document.createElement("div");
        movieDiv.classList.add("movie");

        const title = document.createElement("h2");
        movieDiv.classList.add("title");
        title.textContent = `${movie.title} (${movie.year})`;
        movieDiv.appendChild(title);

        const img = document.createElement("img");
        img.src = movie.image_url;
        img.alt = movie.title;
        movieDiv.appendChild(img);
        if (movieReviews.length > 0) {
          const ratingDiv = document.createElement("div");
          ratingDiv.classList.add("stars");
          let fullStars = (movieReviews[0].stars);
          fullStars = 5-fullStars;
          for (let i = 1; i <= 5; i++) {
            const star = document.createElement("span");
            star.classList.add("star");
            star.innerHTML = i > fullStars ? "&#9733;" : "&#9734;";
            ratingDiv.appendChild(star);
          }
          movieDiv.appendChild(ratingDiv);

          const opinion = document.createElement("p");
          opinion.textContent = movieReviews[0].opinion;
          movieDiv.appendChild(opinion);

          const editBtn = document.createElement("button");
          editBtn.textContent = "Edit Review";
          editBtn.classList.add("openBtn");
          editBtn.setAttribute("data-id", movie.id);
          movieDiv.appendChild(editBtn);
        }
        else {
          const AddReview = document.createElement("button");
          AddReview.textContent = "Add Review";
          AddReview.classList.add("openBtn");
          AddReview.setAttribute("data-id", movie.id);
          movieDiv.appendChild(AddReview);
        }
        container.appendChild(movieDiv);
      });
    });

  // const openBtns = document.querySelectorAll(".openBtn");
  const closeBtns = document.querySelectorAll(".closeBtn");
  const popupBox = document.querySelector(".popupBox");
  const form = document.getElementById("reviewForm");
  const stars = document.querySelectorAll(".star");
  const Countstar = document.getElementById("starsInput");
  console.log("Stars:");
  let selectedStars = 0;

  document.addEventListener("click", (event) => {
    if (event.target.classList.contains("openBtn")) {
      popupBox.style.display = "flex";
      const movieId = event.target.attributes[1].value;
      if(event.target.textContent === "Edit Review"){
        fetch('/reviewData/')
          .then(response => response.json())
          .then(data => {
            const reviews = data.reviews;
            const reviewData = reviews.find(review => review.movie_id == event.target.attributes[1].value);
            document.getElementById("myNote").value = reviewData.opinion;
            document.getElementById("starsInput").value=reviewData.stars;
            highlightStars(reviewData.stars);
          });
        form.action = `/edit_review/${movieId}/`;
      }
      else{
        console.log("Add review clicked for:");
        highlightStars(0);
        form.action = `/add_review/${movieId}/`;
      }
    }
  });
  closeBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      popupBox.style.display = "none";
    });
  });

  popupBox.addEventListener("click", (e) => {
    if (e.target === popupBox) {
      popupBox.style.display = "none";
    }
  });

  stars.forEach((star, index) => {
    star.addEventListener("click", () => {
      selectedStars = 5-index;
      Countstar.value = selectedStars;
      highlightStars(selectedStars);
    });
  });

  function highlightStars(count) {
    // count -= 2;
    count=5-count;
    console.log("Highlighting stars up to:", count);
    stars.forEach((star, i) => {
      console.log("i:", i);
      star.style.color = i >= count ? "gold" : "#444"; // proper highlight
    star.classList.toggle("selected", i < count);
    });
  }
});
