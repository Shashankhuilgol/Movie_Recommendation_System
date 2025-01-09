from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load movie data
with open("movies.json", "r") as file:
    movies = json.load(file)

# Get available languages dynamically from the movie data
available_languages = set(movie["language"] for movie in movies)

@app.route("/")
def home():
    return render_template("index.html", languages=available_languages)

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
        if min_rating and movie.get("rating", 0) < float(min_rating):
            continue

        # Apply language filter
        if language and movie.get("language", "").lower() != language.lower():
            continue

        recommendations.append(movie)

    return render_template("results.html", movies=recommendations, error=None)

if __name__ == "__main__":
    app.run(debug=True)