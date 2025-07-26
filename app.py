from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
import requests

app = Flask(__name__)

# Load movie data and similarity model
try:
    movies = pickle.load(open('Models/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('Models/similarity.pkl', 'rb'))
    movie_df = pd.DataFrame(movies)
except FileNotFoundError:
    print("⚠️ Error: Movie dataset files not found! Ensure 'movie_list.pkl' and 'similarity.pkl' exist.")
    exit(1)

# TMDb API
API_KEY = 'ea76d6ce89f4c765df88f3ad8e9f3018'  # Replace with your actual API key

def fetch_movie_details(movie_id, retries=3):
    """Fetch movie details from TMDb or fallback to local dataset"""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}&language=en-US"

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        movie_data = response.json()

        credits_response = requests.get(credits_url, timeout=20)
        credits_response.raise_for_status()
        credits_data = credits_response.json()

        cast_list = [actor['name'] for actor in credits_data.get('cast', [])[:5]]
        director_list = [crew['name'] for crew in credits_data.get('crew', []) if crew['job'] == "Director"]

        return {
            'movie_id': movie_id,
            'poster_url': f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path', '')}",
            'rating': movie_data.get('vote_average', 'No Rating Available'),
            'title': movie_data.get('title', 'Title Not Available'),
            'release_date': movie_data.get('release_date', 'Date Not Available'),
            'genres': ', '.join([genre['name'] for genre in movie_data.get('genres', [])]) or 'Genres Not Available',
            'production_companies': ', '.join([comp['name'] for comp in movie_data.get('production_companies', [])]) or 'Production Details Not Available',
            'cast': ', '.join(cast_list) or 'Cast Not Available',
            'director': ', '.join(director_list) or 'Director Not Available'
        }

    except requests.exceptions.RequestException as e:
        print(f"⚠️ TMDb fetch failed: {e}")
        # Fallback to dataset
        fallback = movie_df[movie_df['movie_id'] == movie_id]
        if not fallback.empty:
            row = fallback.iloc[0]
            return {
                'movie_id': movie_id,
                'poster_url': '',  # Poster not available offline
                'rating': 'N/A',
                'title': row.get('title', 'Unknown'),
                'release_date': 'N/A',
                'genres': row.get('genres', 'N/A'),
                'production_companies': 'N/A',
                'cast': row.get('cast', 'N/A'),
                'director': row.get('crew', 'N/A')
            }
        return {'movie_id': movie_id, 'poster_url': '', 'rating': 'No Rating Available', 'title': 'Title Not Available'}

def recommend(movie_title):
    """ Provide movie recommendations based on similarity """
    movie_title = movie_title.lower()
    matches = movie_df[movie_df['title'].str.lower() == movie_title]

    if matches.empty:
        return None

    index = matches.index[0]
    distances = list(enumerate(similarity[index]))
    distances = sorted(distances, key=lambda x: x[1], reverse=True)[1:7]

    recommendations = []
    for i in distances:
        if 'movie_id' not in movie_df.columns:
            continue  

        movie_id = movie_df.iloc[i[0]]['movie_id']
        details = fetch_movie_details(movie_id)
        recommendations.append(details)

    return recommendations if recommendations else None

@app.route("/", methods=["GET", "POST"])
def index():
    """ Handle movie search and recommendation rendering """
    if request.method == "POST":
        user_input = request.form.get("movie", "").strip()
        recommendations = recommend(user_input)

        if recommendations is None:
            return render_template("index.html", error="Movie not found. Please try another.")

        return render_template("recommend.html", movie=user_input, recommendations=recommendations)

    return render_template("index.html")

@app.route("/movie/<int:movie_id>")
def movie_details(movie_id):
    """ Fetch full movie details and return JSON response """
    details = fetch_movie_details(movie_id)
    return jsonify(details)

@app.route("/autosuggest", methods=["GET"])
def autosuggest():
    """ Provide autosuggestions for movie search """
    query = request.args.get('query', '').strip().lower()

    if not query:
        return jsonify({'suggestions': []})

    suggestions = movie_df[movie_df['title'].str.lower().str.startswith(query)]['title'].head(5).tolist()
    return jsonify({'suggestions': suggestions})  

if __name__ == "__main__":
    app.run(debug=True)
