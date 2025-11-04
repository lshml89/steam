# src/recursive_utils.py
from sklearn.tree import _tree
from typing import List, Tuple

def tree_to_rules(tree, feature_names: List[str]) -> List[Tuple[List[str], object]]:
    """Extrae reglas del árbol de decisión recursivamente.
    Retorna lista de (condiciones, value) para hojas."""
    tree_ = tree.tree_
    feature_name = [feature_names[i] if i != _tree.TREE_UNDEFINED else 'undefined!' for i in tree_.feature]
    paths = []

    def recurse(node, path):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            recurse(tree_.children_left[node], path + [f"({name} <= {threshold:.3f})"])
            recurse(tree_.children_right[node], path + [f"({name} > {threshold:.3f})"])
        else:
            value = tree_.value[node]
            paths.append((path, value))

    recurse(0, [])
    return paths
