# src/evaluate.py
from typing import List, Set
import math

def precision_at_k(recommended: List[int], relevant: Set[int], k: int = 10) -> float:
    recommended_k = recommended[:k]
    if not recommended_k:
        return 0.0
    return sum([1 for r in recommended_k if r in relevant]) / k

def recall_at_k(recommended: List[int], relevant: Set[int], k: int = 10) -> float:
    if not relevant:
        return 0.0
    recommended_k = recommended[:k]
    return sum([1 for r in recommended_k if r in relevant]) / len(relevant)

def apk(actual: List[int], predicted: List[int], k: int = 10) -> float:
    # Average precision at k
    if not actual:
        return 0.0
    score = 0.0
    num_hits = 0.0
    for i, p in enumerate(predicted[:k]):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)
    return score / min(len(actual), k)
