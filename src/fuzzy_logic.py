import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def calculate_fuzzy_preferences(genre, duration, average_rating, release_year=None):
    # Define input variables
    genre_var = ctrl.Antecedent(np.arange(0, 11, 1), 'genre')
    duration_var = ctrl.Antecedent(np.arange(0, 301, 1), 'duration')  # Extend range to 300
    rating_var = ctrl.Antecedent(np.arange(0, 6, 1), 'average_rating')

    # Define output variable
    recommendation_var = ctrl.Consequent(np.arange(0, 11, 1), 'recommendation')

    # Define membership functions
    genre_var['Action'] = fuzz.trapmf(genre_var.universe, [0, 0, 3, 5])
    genre_var['Comedy'] = fuzz.trapmf(genre_var.universe, [3, 5, 7, 10])
    genre_var['Drama'] = fuzz.trapmf(genre_var.universe, [2, 4, 6, 8])

    duration_var['Short'] = fuzz.trapmf(duration_var.universe, [0, 0, 60, 120])
    duration_var['Medium'] = fuzz.trapmf(duration_var.universe, [60, 120, 180, 240])
    duration_var['Long'] = fuzz.trapmf(duration_var.universe, [120, 240, 300, 300])

    rating_var['Low'] = fuzz.trapmf(rating_var.universe, [0, 0, 1.5, 3.0])
    rating_var['Medium'] = fuzz.trapmf(rating_var.universe, [1.5, 2.5, 3.5, 4.5])
    rating_var['High'] = fuzz.trapmf(rating_var.universe, [3.0, 4.0, 5.0, 5.0])

    recommendation_var['No'] = fuzz.trimf(recommendation_var.universe, [0, 0, 5])
    recommendation_var['Maybe'] = fuzz.trimf(recommendation_var.universe, [2, 5, 8])
    recommendation_var['Yes'] = fuzz.trimf(recommendation_var.universe, [5, 10, 10])

    # Define fuzzy rules
    rules = [
        ctrl.Rule(genre_var['Action'] & duration_var['Short'] & rating_var['High'], recommendation_var['Yes']),
        ctrl.Rule(genre_var['Comedy'] & duration_var['Long'] & rating_var['Low'], recommendation_var['No']),
        ctrl.Rule(genre_var['Drama'] & duration_var['Medium'] & rating_var['Medium'], recommendation_var['Maybe']),
        ctrl.Rule(genre_var['Action'] & duration_var['Medium'] & rating_var['Medium'], recommendation_var['Yes']),
        ctrl.Rule(genre_var['Comedy'] & duration_var['Short'] & rating_var['High'], recommendation_var['Yes']),
        ctrl.Rule(genre_var['Drama'] & duration_var['Long'] & rating_var['Low'], recommendation_var['No']),
        ctrl.Rule(genre_var['Action'] & duration_var['Long'] & rating_var['Low'], recommendation_var['Maybe']),
        ctrl.Rule(genre_var['Comedy'] & duration_var['Medium'] & rating_var['High'], recommendation_var['Yes']),
        ctrl.Rule(genre_var['Drama'] & duration_var['Short'] & rating_var['Medium'], recommendation_var['Maybe']),
        ctrl.Rule(genre_var['Action'] & duration_var['Short'] & rating_var['Low'], recommendation_var['No']),
        ctrl.Rule(genre_var['Comedy'] & duration_var['Short'] & rating_var['Low'], recommendation_var['No']),
        ctrl.Rule(genre_var['Drama'] & duration_var['Short'] & rating_var['High'], recommendation_var['Yes']),
        ctrl.Rule(genre_var['Action'] & duration_var['Long'] & rating_var['High'], recommendation_var['Yes']),
        ctrl.Rule(genre_var['Comedy'] & duration_var['Long'] & rating_var['High'], recommendation_var['Yes']),
        ctrl.Rule(genre_var['Drama'] & duration_var['Long'] & rating_var['High'], recommendation_var['Yes']),
    ]

    # Additional rules for release_year if provided
    if release_year:
        year_var = ctrl.Antecedent(np.arange(1900, 2023, 1), 'release_year')
        year_var['Old'] = fuzz.trapmf(year_var.universe, [1900, 1900, 1950, 1980])
        year_var['Recent'] = fuzz.trapmf(year_var.universe, [1980, 2000, 2022, 2022])
        rules.append(ctrl.Rule(year_var['Old'], recommendation_var['No']))
        rules.append(ctrl.Rule(year_var['Recent'] & rating_var['High'], recommendation_var['Yes']))
        recommendation_ctrl = ctrl.ControlSystem(rules)
    else:
        recommendation_ctrl = ctrl.ControlSystem(rules)

    recommendation_sim = ctrl.ControlSystemSimulation(recommendation_ctrl)

    # Input values
    recommendation_sim.input['genre'] = 5 if genre == 'Action' else 10 if genre == 'Comedy' else 6
    recommendation_sim.input['duration'] = duration
    recommendation_sim.input['average_rating'] = average_rating
    if release_year:
        recommendation_sim.input['release_year'] = release_year

    # Compute result
    try:
        recommendation_sim.compute()
        return recommendation_sim.output['recommendation']
    except ValueError as e:
        print(f"Error computing fuzzy output: {e}")
        return 0  # Default value or handle error appropriately
