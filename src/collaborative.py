# src/collaborative.py
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

class CollaborativeFiltering:
    def __init__(self, ratings: pd.DataFrame):
        self.ratings = ratings.copy()
        self.user_index = {}
        self.item_index = {}
        self.user_item = None

    def build_matrix(self):
        users = sorted(self.ratings['user_id'].unique())
        items = sorted(self.ratings['movie_id'].unique())
        self.user_index = {u:i for i,u in enumerate(users)}
        self.item_index = {m:i for i,m in enumerate(items)}

        mat = np.zeros((len(users), len(items)), dtype=float)
        for row in self.ratings.itertuples(index=False):
            u = self.user_index[row.user_id]
            i = self.item_index[row.movie_id]
            mat[u, i] = row.rating
        self.user_item = csr_matrix(mat)

    def predict_user_based(self, user_id: int, top_k: int = 10):
        if self.user_item is None:
            self.build_matrix()
        uid = self.user_index.get(user_id)
        if uid is None:
            return []
        user_vec = self.user_item[uid]
        sim = cosine_similarity(self.user_item, user_vec).flatten()
        sim[uid] = 0  # ignore self-similarity

        # Weighted sum of ratings
        mat_dense = self.user_item.toarray()
        scores = sim.dot(mat_dense) / (np.abs(sim).sum() + 1e-9)
        ranked = np.argsort(-scores)
        inv_item_index = {v:k for k,v in self.item_index.items()}
        recommendations = [(int(inv_item_index[i]), float(scores[i])) for i in ranked[:top_k]]
        return recommendations

    def predict_item_based(self, movie_id: int, top_k: int = 10):
        # Item-item via cosine on item columns
        if self.user_item is None:
            self.build_matrix()
        if movie_id not in self.item_index:
            return []
        item_mat = self.user_item.toarray().T  # items x users
        idx = self.item_index[movie_id]
        sims = cosine_similarity(item_mat[idx:idx+1], item_mat).flatten()
        sims[idx] = 0
        top = sims.argsort()[::-1][:top_k]
        inv_item_index = {v:k for k,v in self.item_index.items()}
        return [(int(inv_item_index[i]), float(sims[i])) for i in top]

# Wrapper para UI / scripts externos
def recommend_user_based(user_id, ratings, movies, k=5):
    """
    Devuelve un DataFrame con las top-k recomendaciones de un usuario.
    """
    cf = CollaborativeFiltering(ratings)
    cf.build_matrix()
    recs = cf.predict_user_based(user_id, top_k=k)

    rec_list = []
    for movie_id, score in recs:
        title = movies[movies['movie_id'] == movie_id]['title'].values
        title = title[0] if len(title) > 0 else f"Movie {movie_id}"
        rec_list.append({'movie_id': movie_id, 'title': title, 'score': score})
    return pd.DataFrame(rec_list)
