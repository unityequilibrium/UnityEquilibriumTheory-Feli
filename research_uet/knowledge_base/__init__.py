"""
research_uet.knowledge_base
============================
UET Multi-Agent RAG Knowledge Base.

Modules:
    api_client      — OpenRouter API client + CostTracker
    tensorizer      — UET physics → vectors (Ω, κ, β, axioms)
    vector_store    — Hybrid vector store (LanceDB / SQLite)
    omega_search    — Ω-minimization similarity search
    ingest          — Bulk ingestion pipeline
    cost_dashboard  — API cost monitoring CLI

Usage:
    from research_uet.knowledge_base import VectorStore, UetTensorizer, OmegaSearch
"""

__version__ = "0.8.7"

# Lazy imports to avoid loading everything on package import
__all__ = [
    "VectorStore",
    "VectorDocument",
    "UetTensorizer",
    "UetVector",
    "OmegaSearch",
    "IngestionPipeline",
    "CostDashboard",
    "OpenRouterClient",
    "CostTracker",
]


def __getattr__(name):
    """Lazy-load modules on first access."""
    if name in ("VectorStore", "VectorDocument", "SearchResult"):
        from .vector_store import VectorStore, VectorDocument, SearchResult

        return locals()[name]
    elif name in ("UetTensorizer", "UetVector"):
        from .tensorizer import UetTensorizer, UetVector

        return locals()[name]
    elif name in ("OmegaSearch", "compute_omega_distance"):
        from .omega_search import OmegaSearch, compute_omega_distance

        return locals()[name]
    elif name == "IngestionPipeline":
        from .ingest import IngestionPipeline

        return IngestionPipeline
    elif name == "CostDashboard":
        from .cost_dashboard import CostDashboard

        return CostDashboard
    elif name in ("OpenRouterClient", "CostTracker"):
        from .api_client import OpenRouterClient, CostTracker

        return locals()[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
