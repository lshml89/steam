# src/features.py
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer

def build_content_matrix(movies_df):
    """
    Construye una matriz TF-IDF basada en descripción + géneros
    """
    # Asegurar que genres está en formato lista
    movies = movies_df.copy()
    movies['genres'] = movies['genres'].apply(lambda g: g.split('|') if isinstance(g, str) else [])

    # TF-IDF sobre descripción
    tf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tf.fit_transform(movies['description'])

    # One-hot para géneros
    mlb = MultiLabelBinarizer()
    genre_matrix = mlb.fit_transform(movies['genres'])

    # Convertimos todo a numpy array para evitar np.matrix
    tfidf_matrix = tfidf_matrix.toarray()
    genre_matrix = np.asarray(genre_matrix)

    # Unimos TF-IDF + géneros
    content_matrix = np.hstack([tfidf_matrix, genre_matrix])

    return content_matrix, tf, mlb


def build_user_profile(X_content, movies_df, liked_movie_ids):
    """
    Construye perfil promedio basado en películas que le gustaron al usuario
    """
    # Indices de las películas que el usuario marcó con 4 estrellas o más
    idxs = movies_df.index[movies_df['movie_id'].isin(liked_movie_ids)].tolist()

    if not idxs:
        return None

    # Seleccionamos vectores
    vecs = X_content[idxs]

    # Promedio → perfil del usuario
    profile = np.mean(vecs, axis=0)

    return profile.reshape(1, -1)
