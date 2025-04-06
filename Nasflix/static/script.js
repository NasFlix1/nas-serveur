const API_URL = "http://localhost:2000"; // URL de ton API Flask

// Charger les films depuis l'API
async function loadMovies() {
    const response = await fetch(`${API_URL}/movies`);
    const movies = await response.json();
    const movieList = document.getElementById("movies-list");

    movieList.innerHTML = ""; // Vider la liste
    movies.forEach(movie => {
        const movieElement = document.createElement("div");
        movieElement.classList.add("movie");
        movieElement.innerHTML = `<img src="https://via.placeholder.com/150" alt="${movie.name}">`; // Image temporaire

        // Charger les détails du film
        movieElement.addEventListener("click", async () => {
            const details = await fetchMovieDetails(movie.name);
            if (details) {
                showMovieDetails(details);
            }
        });

        movieList.appendChild(movieElement);
    });
}

// Récupérer les détails d'un film
async function fetchMovieDetails(name) {
    const response = await fetch(`${API_URL}/movie/${encodeURIComponent(name)}`);
    if (response.ok) {
        return response.json();
    } else {
        alert("Film non trouvé !");
        return null;
    }
}

// Afficher les détails du film sélectionné
function showMovieDetails(movie) {
    document.getElementById("title").innerText = movie.title;
    document.getElementById("year").innerText = `Année : ${movie.year}`;
    document.getElementById("description").innerText = movie.description;
    document.getElementById("movie-details").classList.remove("hidden");

    // Changer l'image et le fond
    document.getElementById("background").style.backgroundImage = `url(${movie.background})`;

    // Changer la pochette du film cliqué
    const movieImages = document.querySelectorAll(".movie img");
    movieImages.forEach(img => {
        if (img.alt === movie.title) {
            img.src = movie.poster;
        }
    });
}

// Charger les films au démarrage
window.onload = loadMovies;

