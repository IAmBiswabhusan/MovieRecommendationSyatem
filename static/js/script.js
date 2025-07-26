document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ JS Loaded - Checking More Details Buttons");

    const input = document.getElementById("movie-input");
    const suggestionsBox = document.getElementById("suggestions");

    // Autosuggestion Handler
    if (input && suggestionsBox) {
        input.addEventListener("input", async () => {
            const query = input.value.trim();
            if (query.length < 1) {
                suggestionsBox.style.display = "none";
                return;
            }

            try {
                const response = await fetch(`/autosuggest?query=${encodeURIComponent(query)}`);
                const data = await response.json();
                const suggestions = data.suggestions;

                suggestionsBox.innerHTML = suggestions.length
                    ? suggestions.map(title => `<li onclick="selectSuggestion('${title}')">${title}</li>`).join("")
                    : "<li class='disabled'>No matches found</li>";

                suggestionsBox.style.display = "block";
            } catch (error) {
                console.error("❌ Error fetching suggestions:", error);
            }
        });

        window.selectSuggestion = function (title) {
            input.value = title;
            suggestionsBox.style.display = "none";
        };
    }

    // More Details Modal Functionality
    document.querySelectorAll(".more-details-btn").forEach(button => {
        button.addEventListener("click", async (event) => {
            const movieId = event.target.getAttribute("data-movie-id");
            console.log("🔍 Clicked 'More Details' for Movie ID:", movieId);

            if (!movieId) {
                console.error("❌ No movie ID found for More Details button.");
                return;
            }

            try {
                const response = await fetch(`/movie/${movieId}`);
                if (!response.ok) {
                    console.error(`❌ Failed to fetch movie details. Status: ${response.status}`);
                    return;
                }

                const movie = await response.json();
                console.log("✅ Movie Data Fetched:", movie);

                // Ensure modal elements exist before modifying them
                const modalTitle = document.getElementById("modalTitle");
                const modalPoster = document.getElementById("modalPoster");
                const modalReleaseDate = document.getElementById("modalReleaseDate");
                const modalGenres = document.getElementById("modalGenres");
                const modalProduction = document.getElementById("modalProduction");
                const modalCast = document.getElementById("modalCast");
                const modalDirector = document.getElementById("modalDirector");

                if (!modalTitle || !modalPoster || !modalReleaseDate || !modalGenres || !modalProduction || !modalCast || !modalDirector) {
                    console.error("❌ Modal elements not found in DOM.");
                    return;
                }

                // Populate modal with movie details
                modalTitle.innerText = movie.title || "Title Not Available";
                modalPoster.src = movie.poster_url || "https://via.placeholder.com/300x450?text=No+Image+Available";
                modalReleaseDate.innerText = movie.release_date || "Date Not Available";
                modalGenres.innerText = movie.genres || "Genres Not Available";
                modalProduction.innerText = movie.production_companies || "Production Details Not Available";
                modalCast.innerText = movie.cast || "Cast Not Available";
                modalDirector.innerText = movie.director || "Director Not Available";

                // Show the modal
                new bootstrap.Modal(document.getElementById("movieModal")).show();

            } catch (error) {
                console.error("❌ Error fetching movie details:", error);
            }
        });
    });
});