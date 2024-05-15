from flask import Flask, request, render_template, flash, redirect, url_for
import pandas as pd
from recommender import Movie, Preferences, Recommendation
from fuzzy_logic import calculate_fuzzy_preferences
import os

app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = 'supersecretkey'  # Necessario per flash messages

# Load the dataset
movies = pd.read_csv('data/movies.csv')
ratings = pd.read_csv('data/ratings.csv')

# Preprocess the movie data
movie_list = []
for index, row in movies.iterrows():
    # Extract the duration and average rating from the ratings dataframe
    movie_ratings = ratings[ratings['movieId'] == row['movieId']]
    average_rating = movie_ratings['rating'].mean()
    duration = 120  # Assuming a default duration; replace with actual data if available

    movie = Movie(row['movieId'], row['title'], row['genres'], duration, average_rating)
    movie_list.append(movie)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    genre = request.form['genre']
    duration = request.form['duration']
    rating = request.form['rating']
    release_year = request.form.get('release_year')

    # Validate inputs
    if not genre:
        flash('Genre is required.')
        return redirect(url_for('index'))

    try:
        duration = int(duration)
        if duration < 1 or duration > 300:
            flash('Duration must be between 1 and 300 minutes.')
            return redirect(url_for('index'))
    except ValueError:
        flash('Invalid duration value.')
        return redirect(url_for('index'))

    try:
        rating = float(rating)
        if rating < 0 or rating > 5:
            flash('Rating must be between 0 and 5.')
            return redirect(url_for('index'))
    except ValueError:
        flash('Invalid rating value.')
        return redirect(url_for('index'))

    if release_year:
        try:
            release_year = int(release_year)
            if release_year < 1900 or release_year > 2022:
                flash('Release year must be between 1900 and 2022.')
                return redirect(url_for('index'))
        except ValueError:
            flash('Invalid release year value.')
            return redirect(url_for('index'))
    else:
        release_year = None

    # Define user preferences
    user_preferences = Preferences(genre, duration, rating)

    # Calculate fuzzy preferences
    fuzzy_score = calculate_fuzzy_preferences(user_preferences.genre, user_preferences.duration,
                                              user_preferences.average_rating, release_year)

    # Create a recommendation system
    recommendation = Recommendation(user_preferences, movie_list)

    # Generate suggestions
    suggestions = recommendation.generate_suggestions()

    return render_template('results.html', suggestions=suggestions, fuzzy_score=fuzzy_score)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
