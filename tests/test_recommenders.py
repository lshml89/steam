# tests/test_recommenders.py
from src.data_processing import load_data
from src.features import build_content_matrix, build_user_profile
from src.content_based import ContentBased
from src.collaborative import CollaborativeFiltering

def test_content_recommender_runs():
    movies, ratings = load_data('data')
    X, tf, mlb = build_content_matrix(movies)
    cb = ContentBased(X, movies)
    # pick a movie that exists
    mid = int(movies.iloc[0]['movie_id'])
    recs = cb.recommend_for_movie(mid, top_k=5)
    assert isinstance(recs, list)

def test_collab_recommender_runs():
    movies, ratings = load_data('data')
    collab = CollaborativeFiltering(ratings)
    collab.build_matrix()
    # pick an existing user
    uid = int(ratings.iloc[0]['user_id'])
    recs = collab.predict_user_based(uid, top_k=5)
    assert isinstance(recs, list)
