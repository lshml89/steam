# tests/test_data_processing.py
from src.data_processing import load_data

def test_load_data_non_empty():
    movies, ratings = load_data('data')
    assert not movies.empty
    assert not ratings.empty
    assert 'movie_id' in movies.columns
    assert 'user_id' in ratings.columns
