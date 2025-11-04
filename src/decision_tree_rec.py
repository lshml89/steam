# src/decision_tree_rec.py
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from typing import Any

class DecisionTreeRec:
    def __init__(self, max_depth: int = 6, random_state: int = 42):
        self.clf = DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
        self.feature_names = None

    def fit(self, X, y, feature_names=None):
        """X: np.ndarray or sparse, y: binary labels (1 like, 0 dislike)"""
        self.feature_names = feature_names
        self.clf.fit(X, y)

    def predict(self, X):
        return self.clf.predict(X)

    def predict_proba(self, X):
        return self.clf.predict_proba(X)[:, 1]

    def export_rules(self):
        # Usar recursive_utils.tree_to_rules si quieres reglas legibles
        return self.clf
