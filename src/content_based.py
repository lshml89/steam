# src/content_based.py
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

class ContentBased:
    def __init__(self, content_matrix, movies_df):
        # Convertimos todo a array para evitar errores de np.matrix
        self.X = np.asarray(content_matrix)
        self.movies = movies_df.reset_index(drop=True)

    def recommend_for_movie(self, movie_id, top_k=10):
        idxs = self.movies.index[self.movies['movie_id'] == movie_id].tolist()
        if not idxs:
            return []
        i = idxs[0]

        # Convertimos vector a forma correcta
        movie_vec = self.X[i].reshape(1, -1)
        sims = cosine_similarity(movie_vec, self.X).flatten()

        sims[i] = 0  # evitar recomendar la misma película
        top = sims.argsort()[::-1][:top_k]
        return [(int(self.movies.iloc[j]['movie_id']), float(sims[j])) for j in top]

    def recommend_for_user_profile(self, user_profile_vector, top_k=10):
        if user_profile_vector is None:
            return []

        # 🔥 Aquí corregimos el error: convertimos np.matrix → np.array
        user_profile_vector = np.asarray(user_profile_vector).reshape(1, -1)

        sims = cosine_similarity(user_profile_vector, self.X).flatten()
        top = sims.argsort()[::-1][:top_k]

        return [(int(self.movies.iloc[j]['movie_id']), float(sims[j])) for j in top]


# Wrapper para UI / scripts externos
def recommend_by_content(user_id, ratings, movies, k=5):
    """
    Devuelve un DataFrame con las top-k recomendaciones usando contenido.
    """
    from features import build_content_matrix, build_user_profile

    X_content, tf, mlb = build_content_matrix(movies)
    X_content = np.asarray(X_content)  # prevenir np.matrix

    liked = ratings[(ratings['user_id'] == user_id) & (ratings['rating'] >= 4)]['movie_id'].tolist()

    if not liked:
        return pd.DataFrame(columns=['movie_id','title','score'])

    profile = build_user_profile(X_content, movies, liked)
    profile = np.asarray(profile)  # prevenir np.matrix

    cb = ContentBased(X_content, movies)
    recs = cb.recommend_for_user_profile(profile, top_k=k)

    rec_list = []
    for movie_id, score in recs:
        title = movies[movies['movie_id'] == movie_id]['title'].values
        title = title[0] if len(title) > 0 else f"Movie {movie_id}"
        rec_list.append({'movie_id': movie_id, 'title': title, 'score': score})

    return pd.DataFrame(rec_list)
