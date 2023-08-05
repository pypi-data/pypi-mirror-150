"""Submodule providing experiments pipelines."""
from .compute_node_embedding import (
    compute_node_embedding,
    get_available_node_embedding_methods
)
from .edge_prediction import evaluate_embedding_for_edge_prediction
from .node_label_prediction import node_label_prediction

__all__ = [
    "compute_node_embedding",
    "get_available_node_embedding_methods",
    "evaluate_embedding_for_edge_prediction",
    "node_label_prediction"
]