# src/api.py
from flask import Flask, jsonify
from src.data_processing import load_data, get_user_profile
from src.features import build_content_matrix, build_user_profile
from src.content_based import ContentBased

app = Flask(__name__)

# Cargar datos y modelos al iniciar (prototipo)
movies, ratings = load_data('data')
X_content, tf, mlb = build_content_matrix(movies)
cb = ContentBased(X_content, movies)

@app.route('/recommend/content/<int:user_id>', methods=['GET'])
def recommend_content(user_id):
    liked = get_user_profile(ratings, user_id, threshold=4.0)
    if not liked:
        return jsonify({'user_id': user_id, 'recommendations': []})
    profile = build_user_profile(X_content, movies, liked)
    recs = cb.recommend_for_user_profile(profile, top_k=10)
    recommendations = [{'movie_id': mid, 'score': score} for mid, score in recs]
    return jsonify({'user_id': user_id, 'recommendations': recommendations})

# Minimal wrapper for collaborative (if se construye dinámicamente)
from src.collaborative import CollaborativeFiltering
_collab = None
def get_collab():
    global _collab
    if _collab is None:
        _collab = CollaborativeFiltering(ratings)
        _collab.build_matrix()
    return _collab

@app.route('/recommend/collab/<int:user_id>', methods=['GET'])
def recommend_collab(user_id):
    collab = get_collab()
    recs = collab.predict_user_based(user_id, top_k=10)
    recommendations = [{'movie_id': mid, 'score': score} for mid, score in recs]
    return jsonify({'user_id': user_id, 'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
