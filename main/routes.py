from flask import request, render_template, flash, redirect, url_for
from main import main
from models.recommender import Movie as MovieData, Preferences, Recommendation
from models.fuzzy_logic import calculate_fuzzy_preferences
import requests
from tmdbv3api import TMDb, Movie

tmdb = TMDb()
tmdb.api_key = '3cb5d394e8eb3ae4351dc3c13249a5a9'
tmdb.language = 'en'
tmdb.debug = True
movie_api = Movie()

def get_movie_credits(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={tmdb.api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_movie_data(movie_id):
    movie_details = movie_api.details(movie_id)
    credits = get_movie_credits(movie_id)
    director = None
    if credits:
        for crew_member in credits.get('crew', []):
            if crew_member.get('job') == 'Director':
                director = crew_member.get('name')
                break
    return {
        'movie_id': movie_id,
        'title': movie_details.title,
        'genres': ', '.join([genre['name'] for genre in movie_details.genres]),
        'release_year': movie_details.release_date.split('-')[0] if movie_details.release_date else None,
        'duration': movie_details.runtime,
        'average_rating': movie_details.vote_average,
        'director': director
    }

def get_popular_movies():
    movies = movie_api.popular()
    return [get_movie_data(movie.id) for movie in movies]

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/recommend', methods=['POST'])
def recommend():
    genre = request.form['genre']
    duration = request.form['duration']
    rating = request.form['rating']
    release_year = request.form.get('release_year')

    # Validate inputs
    if not genre:
        flash('Genre is required.')
        return redirect(url_for('main.index'))

    try:
        duration = int(duration)
        if duration < 1 or duration > 300:
            flash('Duration must be between 1 and 300 minutes.')
            return redirect(url_for('main.index'))
    except ValueError:
        flash('Invalid duration value.')
        return redirect(url_for('main.index'))

    try:
        rating = float(rating)
        if rating < 0 or rating > 10:
            flash('Rating must be between 0 and 10.')
            return redirect(url_for('main.index'))
    except ValueError:
        flash('Invalid rating value.')
        return redirect(url_for('main.index'))

    if release_year:
        try:
            release_year = int(release_year)
            if release_year < 1900 or release_year > 2022:
                flash('Release year must be between 1900 and 2022.')
                return redirect(url_for('main.index'))
        except ValueError:
            flash('Invalid release year value.')
            return redirect(url_for('main.index'))
    else:
        release_year = None

    # Define user preferences
    user_preferences = Preferences(genre, duration, rating)

    # Calculate fuzzy preferences
    fuzzy_score = calculate_fuzzy_preferences(user_preferences.genre, user_preferences.duration,
                                              user_preferences.average_rating, release_year)

    # Get movie data from API
    movie_list = get_popular_movies()

    # Create a recommendation system
    recommendation = Recommendation(user_preferences, [MovieData(**movie) for movie in movie_list])

    # Generate suggestions
    suggestions = recommendation.generate_suggestions()

    return render_template('results.html', suggestions=suggestions, fuzzy_score=fuzzy_score)
