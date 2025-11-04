# src/data_processing.py
import pandas as pd
from typing import Tuple

def load_data(path: str = 'data') -> Tuple[pd.DataFrame, pd.DataFrame]:
    movies = pd.read_csv(f'{path}/movies.csv')
    ratings = pd.read_csv(f'{path}/ratings.csv')

    # Normalizar y limpiar
    movies['genres'] = movies['genres'].fillna('').apply(lambda s: s.split('|') if s else [])
    movies['title'] = movies['title'].fillna('')
    movies['description'] = movies['description'].fillna('')

    ratings = ratings.dropna(subset=['user_id','movie_id','rating'])
    ratings['rating'] = ratings['rating'].astype(float)
    return movies, ratings

def get_user_profile(ratings, user_id, threshold=4.0):
    """Devuelve lista de movie_id que el usuario 'gusta' (rating >= threshold)."""
    user_r = ratings[ratings['user_id'] == user_id]
    liked = user_r[user_r['rating'] >= threshold]['movie_id'].unique().tolist()
    return liked

if __name__ == '__main__':
    m, r = load_data('data')
    print(m.head())
    print(r.head())
