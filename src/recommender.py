class Movie:
    def __init__(self, movie_id, title, genre, duration, average_rating):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.duration = duration
        self.average_rating = average_rating

    def __str__(self):
        return f"{self.title} ({self.genre}, {self.duration} min, Rating: {self.average_rating})"


class Preferences:
    def __init__(self, genre, duration, average_rating):
        self.genre = genre
        self.duration = duration
        self.average_rating = average_rating

    def __str__(self):
        return f"Genre: {self.genre}, Duration: {self.duration} min, Rating: {self.average_rating}"


class Recommendation:
    def __init__(self, preferences, movie_list):
        self.preferences = preferences
        self.movie_list = movie_list

    def generate_suggestions(self):
        suggestions = []
        for movie in self.movie_list:
            if self.match_preferences(movie):
                suggestions.append(movie)
        return suggestions

    def match_preferences(self, movie):
        return (
            self.preferences.genre in movie.genre and
            movie.duration <= self.preferences.duration and
            movie.average_rating >= self.preferences.average_rating
        )
