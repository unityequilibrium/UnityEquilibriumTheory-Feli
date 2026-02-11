"""
UET Knowledge Base
==================
Vector database and search engine for UET research data.
Uses UET physics (Ω, κ, β) for embeddings and similarity search.

Modules:
    - api_client: OpenRouter API client with per-agent cost tracking
    - tensorizer: UET physics → vector embeddings
    - vector_store: LanceDB hybrid store
    - omega_search: Ω-minimization similarity search
    - ingest: Bulk ingestion pipeline
    - cost_dashboard: Cost monitoring CLI
"""

__version__ = "0.1.0"
