import unittest
from recommender import Movie, Preferences, Recommendation

class TestRecommendation(unittest.TestCase):

    def setUp(self):
        self.movie1 = Movie(1, 'Toy Story', 'Animation', 81, 4.0)
        self.movie2 = Movie(2, 'Jumanji', 'Adventure', 104, 3.2)
        self.movie3 = Movie(3, 'Grumpier Old Men', 'Comedy', 101, 3.6)
        self.movies = [self.movie1, self.movie2, self.movie3]
        self.preferences = Preferences('Comedy', 120, 3.5)
        self.recommendation = Recommendation(self.preferences, self.movies)

    def test_generate_suggestions(self):
        suggestions = self.recommendation.generate_suggestions()
        self.assertIn(self.movie3, suggestions)
        self.assertNotIn(self.movie1, suggestions)
        self.assertNotIn(self.movie2, suggestions)

if __name__ == '__main__':
    unittest.main()
