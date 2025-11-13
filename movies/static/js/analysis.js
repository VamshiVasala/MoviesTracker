document.addEventListener("DOMContentLoaded", () => {
const data = JSON.parse(localStorage.getItem("reviewList"));



const container=document.getElementById("movie-container");

const movieCard=document.createElement("div");
movieCard.classList.add("movie");

const title=document.createElement("sh2");
title.classList.add("title");
title.textContent=data[0][0];

movieCard.appendChild(title);

const img=document.createElement("img");
img.classList.add("img");
img.src=data[0][1];

movieCard.appendChild(img); 

container.appendChild(movieCard);

});