# src/cross_validation.py
import numpy as np
from sklearn.model_selection import KFold
from typing import Callable, Dict, Any
import pandas as pd

def k_fold_evaluate(recommender_builder: Callable[[pd.DataFrame], Any],
                    ratings: pd.DataFrame,
                    k: int = 5) -> Dict[str, list]:
    """Recommender_builder debe recibir un DataFrame 'train' y devolver un objeto con método recommend(user_id) -> list(ids)."""
    kf = KFold(n_splits=k, shuffle=True, random_state=42)
    idx = np.arange(len(ratings))
    metrics = {'precision@10': [], 'recall@10': []}

    for train_idx, test_idx in kf.split(idx):
        train = ratings.iloc[train_idx].reset_index(drop=True)
        test = ratings.iloc[test_idx].reset_index(drop=True)
        rec = recommender_builder(train)

        # evaluación básica: para cada usuario en test, comparar recommendations con items en test rated >=4
        users = test['user_id'].unique()
        from src.evaluate import precision_at_k, recall_at_k
        for u in users:
            true_pos = set(test[(test['user_id']==u) & (test['rating']>=4)]['movie_id'].tolist())
            if not true_pos:
                continue
            try:
                recs = rec.recommend(user_id=u, k=10)  # convención mínima
                rec_ids = [r[0] if isinstance(r, (list,tuple)) else r for r in recs]
                metrics['precision@10'].append(precision_at_k(rec_ids, true_pos, k=10))
                metrics['recall@10'].append(recall_at_k(rec_ids, true_pos, k=10))
            except Exception:
                continue

    return metrics
