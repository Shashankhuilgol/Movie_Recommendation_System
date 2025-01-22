from flask import Flask, render_template, request
import json

app = Flask(__name__, static_folder='static')

# Load movie data
with open("movies.json", "r") as file:
    movies = json.load(file)

# Get available genres and languages dynamically from the movie data
available_genres = sorted(set(movie["genre"] for movie in movies if "genre" in movie))
available_languages = sorted(set(movie["language"] for movie in movies if "language" in movie))

@app.route("/")
def home():
    # Pass genres and languages to the home page
    return render_template("index.html", genres=available_genres, languages=available_languages)

@app.route("/recommend", methods=["POST"])
def recommend():
    genre = request.form.get("genre")
    min_rating = request.form.get("rating")
    language = request.form.get("language")

    recommendations = []

    for movie in movies:
        # Apply genre filter
        if genre and movie.get("genre", "").lower() != genre.lower():
            continue

        # Apply rating filter
        if min_rating and float(movie.get("rating", 0)) < float(min_rating):
            continue

        # Apply language filter
        if language and movie.get("language", "").lower() != language.lower():
            continue

        recommendations.append(movie)

    # Pass recommendations and filters back to the results page
    return render_template("results.html", movies=recommendations, genres=available_genres, languages=available_languages)

if __name__ == "__main__":
    app.run(debug=False)
