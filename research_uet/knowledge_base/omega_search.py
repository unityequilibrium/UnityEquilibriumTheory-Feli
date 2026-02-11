"""
Ω-Search Engine — UET Physics-Informed Similarity Search
=========================================================
Finds research documents that minimize the Omega functional Ω
relative to a query, meaning they are at "dynamic equilibrium"
with the query context.

This is the UET-specific innovation:
    Standard RAG: cosine similarity on semantic embeddings
    UET RAG: Ω-minimization on physics-derived vectors

How It Works:
    1. Query text → UET Tensorizer → UetVector (20d)
    2. Compute Ω-distance between query vector and stored vectors
    3. Documents with lowest ΔΩ are most "in equilibrium" with query
    4. Combine with semantic similarity for hybrid ranking

Usage:
    from research_uet.knowledge_base.omega_search import OmegaSearch

    engine = OmegaSearch(vector_store, tensorizer)
    results = engine.search("galaxy rotation curve", top_k=5)

Rust Compatibility:
    - All math is pure float operations (no Python-only dependencies)
    - OmegaDistance is a simple struct
"""

import math
from dataclasses import dataclass
from typing import Optional

import numpy as np

from .tensorizer import UetTensorizer, UetVector
from .vector_store import VectorStore, SearchResult, VectorDocument


# =============================================================================
# Ω-DISTANCE METRIC
# =============================================================================


@dataclass
class OmegaDistance:
    """
    UET Omega-based distance between two vectors.

    Components:
        delta_omega: |Ω_q - Ω_d| — balance difference
        scale_match: 1 if same physical scale, 0 otherwise
        axiom_overlap: Jaccard similarity of axiom signatures
        parameter_dist: Euclidean distance of (κ,β,α,γ)
        entropy_diff: |H_q - H_d| — information density difference

    Combined Distance:
        D = w₁·ΔΩ + w₂·(1-axiom_overlap) + w₃·param_dist + w₄·ΔH - w₅·scale_match
    """

    delta_omega: float
    scale_match: float  # 0.0 or 1.0
    axiom_overlap: float  # 0.0 to 1.0 (Jaccard)
    parameter_dist: float
    entropy_diff: float
    combined: float  # Final weighted distance


def compute_omega_distance(
    query: UetVector,
    document: UetVector,
    weights: Optional[dict[str, float]] = None,
) -> OmegaDistance:
    """
    Compute Ω-distance between a query vector and a document vector.

    Lower distance = more similar = closer to shared equilibrium.

    Args:
        query: Query UET vector
        document: Document UET vector
        weights: Override default component weights

    Returns:
        OmegaDistance with component breakdown
    """
    # Default weights (tuned for research document search)
    w = weights or {
        "omega": 0.30,  # Ω balance is primary signal
        "axiom": 0.25,  # Axiom overlap captures topical relevance
        "params": 0.20,  # Parameter match captures physical scale
        "entropy": 0.15,  # Information density similarity
        "scale": 0.10,  # Bonus for same physical scale
    }

    # 1. ΔΩ — absolute difference in balance functional
    delta_omega = abs(query.omega - document.omega)

    # 2. Scale match — binary
    scale_match = 1.0 if query.scale == document.scale else 0.0

    # 3. Axiom overlap — Jaccard similarity
    q_set = set(i for i, v in enumerate(query.axiom_signature) if v)
    d_set = set(i for i, v in enumerate(document.axiom_signature) if v)
    union = q_set | d_set
    axiom_overlap = len(q_set & d_set) / len(union) if union else 1.0

    # 4. Parameter distance — Euclidean in (κ, β, α, γ) space
    param_q = np.array([query.kappa, query.beta, query.alpha, query.gamma])
    param_d = np.array([document.kappa, document.beta, document.alpha, document.gamma])
    parameter_dist = float(np.linalg.norm(param_q - param_d))

    # 5. Entropy difference
    entropy_diff = abs(query.entropy - document.entropy)
    # Normalize to ~[0, 1] range (max entropy diff ≈ 5 bits)
    entropy_diff_norm = min(entropy_diff / 5.0, 1.0)

    # Normalize delta_omega to ~[0, 1]
    delta_omega_norm = min(delta_omega / 0.5, 1.0)

    # Normalize parameter_dist to ~[0, 1]
    param_dist_norm = min(parameter_dist / 2.0, 1.0)

    # Combined distance (lower = better)
    combined = (
        w["omega"] * delta_omega_norm
        + w["axiom"] * (1.0 - axiom_overlap)
        + w["params"] * param_dist_norm
        + w["entropy"] * entropy_diff_norm
        - w["scale"] * scale_match  # Bonus (reduces distance)
    )

    return OmegaDistance(
        delta_omega=delta_omega,
        scale_match=scale_match,
        axiom_overlap=axiom_overlap,
        parameter_dist=parameter_dist,
        entropy_diff=entropy_diff,
        combined=max(combined, 0.0),  # Clamp to non-negative
    )


# =============================================================================
# Ω-SEARCH ENGINE
# =============================================================================


class OmegaSearch:
    """
    UET Ω-minimization search engine.

    Finds documents that are closest to "dynamic equilibrium"
    with the query, using UET physics metrics.
    """

    def __init__(
        self,
        store: VectorStore,
        tensorizer: UetTensorizer,
        default_top_k: int = 10,
    ):
        self.store = store
        self.tensorizer = tensorizer
        self.default_top_k = default_top_k

    def search(
        self,
        query_text: str,
        top_k: Optional[int] = None,
        topic_hint: str = "0.0",
        omega_weights: Optional[dict[str, float]] = None,
    ) -> list[dict]:
        """
        Search using Ω-minimization — the UET way.

        Args:
            query_text: Natural language query
            top_k: Number of results
            topic_hint: Hint for parameter selection (e.g. "0.1" for astrophysics)
            omega_weights: Override Ω distance weights

        Returns:
            List of search result dicts with Ω breakdown
        """
        top_k = top_k or self.default_top_k

        # 1. Tensorize query
        query_vec = self.tensorizer.tensorize_text(
            query_text, topic_number=topic_hint, label="search_query"
        )

        # 2. Get candidates from UET vector search
        uet_flat = query_vec.to_flat_vector()
        candidates = self.store.search_uet(uet_flat, top_k=top_k * 3)

        # 3. Re-rank by Ω-distance
        results = []
        for candidate in candidates:
            # Reconstruct UetVector from stored data
            doc_uet = self._reconstruct_uet_vector(candidate.doc)

            # Compute Ω-distance
            omega_dist = compute_omega_distance(query_vec, doc_uet, weights=omega_weights)

            results.append(
                {
                    "doc_id": candidate.doc.doc_id,
                    "topic_id": candidate.doc.topic_id,
                    "file_path": candidate.doc.file_path,
                    "title": candidate.doc.title,
                    "omega_distance": omega_dist.combined,
                    "delta_omega": omega_dist.delta_omega,
                    "axiom_overlap": omega_dist.axiom_overlap,
                    "scale_match": omega_dist.scale_match,
                    "parameter_dist": omega_dist.parameter_dist,
                    "entropy_diff": omega_dist.entropy_diff,
                    "doc_omega": candidate.doc.omega,
                    "query_omega": query_vec.omega,
                }
            )

        # Sort by Ω-distance (ascending = most similar)
        results.sort(key=lambda r: r["omega_distance"])
        return results[:top_k]

    def search_by_topic(
        self,
        topic_number: str,
        top_k: Optional[int] = None,
    ) -> list[dict]:
        """
        Find documents most related to a given UET topic.

        Uses the topic's canonical parameters as the query vector.
        """
        top_k = top_k or self.default_top_k

        # Create a "topic-canonical" query
        canonical_text = f"UET topic {topic_number} research analysis"
        return self.search(
            query_text=canonical_text,
            top_k=top_k,
            topic_hint=topic_number,
        )

    def explain_match(self, result: dict) -> str:
        """
        Generate human-readable explanation of why a document matched.

        Returns a formatted string explaining the Ω-distance components.
        """
        lines = [
            f"📄 {result['title'] or result['doc_id']}",
            f"   Topic: {result['topic_id']}",
            f"   Ω-Distance: {result['omega_distance']:.4f}",
            f"   ├── ΔΩ: {result['delta_omega']:.4f} "
            f"(query Ω={result['query_omega']:.4f}, doc Ω={result['doc_omega']:.4f})",
            f"   ├── Axiom overlap: {result['axiom_overlap']:.1%}",
            f"   ├── Scale match: {'✅' if result['scale_match'] else '❌'}",
            f"   ├── Parameter dist: {result['parameter_dist']:.4f}",
            f"   └── Entropy diff: {result['entropy_diff']:.4f}",
        ]
        return "\n".join(lines)

    def _reconstruct_uet_vector(self, doc: VectorDocument) -> UetVector:
        """Reconstruct a UetVector from VectorDocument metadata."""
        return UetVector(
            omega=doc.omega,
            kappa=doc.kappa,
            beta=doc.beta,
            alpha=1.0,  # Default if not stored
            gamma=0.025,  # Default if not stored
            entropy=doc.entropy,
            axiom_signature=[False] * 12,  # Not stored in VectorDocument
            topic_id=doc.topic_id,
            topic_number=doc.topic_number,
            file_path=doc.file_path,
            file_type=doc.file_type,
            content_hash=doc.content_hash,
            char_count=doc.char_count,
            axiom_count=doc.axiom_count,
            scale=doc.scale,
        )


# =============================================================================
# STANDALONE TEST
# =============================================================================

if __name__ == "__main__":
    import tempfile
    import shutil
    from pathlib import Path

    print("=" * 60)
    print("  Ω-Search Engine — Self Test")
    print("=" * 60)

    # Create temp store
    tmp_dir = Path(tempfile.mkdtemp(prefix="uet_omega_"))

    try:
        store = VectorStore(tmp_dir)
        tensorizer = UetTensorizer(grid_size=64)
        engine = OmegaSearch(store, tensorizer)

        # Create test documents with different physics characteristics
        test_docs = [
            ("Galaxy rotation curve analysis using UET κ=0.1", "0.1", "astrophysical"),
            ("Electroweak symmetry breaking and Higgs mechanism", "0.3", "electroweak"),
            ("Quantum entanglement and information coupling β", "0.4", "electroweak"),
            ("Neural dynamics and fluid equilibrium patterns", "0.10", "macroscopic"),
            ("Planck scale black hole entropy calculation", "0.2", "planck"),
        ]

        print("\n--- Indexing test documents ---")
        for i, (text, topic, scale) in enumerate(test_docs):
            uet_vec = tensorizer.tensorize_text(text, topic_number=topic, label=f"doc_{i}")
            doc = VectorDocument(
                doc_id=f"doc_{i}",
                semantic_vec=[0.0] * 8,  # Placeholder
                uet_vec=uet_vec.to_flat_vector(),
                topic_id=f"{topic}_Test",
                topic_number=topic,
                file_path=f"topics/{topic}/test.py",
                file_type="python",
                title=text[:50],
                content_hash=f"hash_{i}",
                char_count=len(text),
                omega=uet_vec.omega,
                kappa=uet_vec.kappa,
                beta=uet_vec.beta,
                entropy=uet_vec.entropy,
                axiom_count=uet_vec.axiom_count,
                scale=uet_vec.scale,
            )
            store.add(doc)
            print(
                f"  [{i}] {topic} → Ω={uet_vec.omega:.4f}, κ={uet_vec.kappa}, axioms={uet_vec.axiom_count}"
            )

        # Test: Ω-search
        print(f"\n--- Test 1: Ω-search for 'galaxy rotation' ---")
        results = engine.search("galaxy rotation curve dark matter", topic_hint="0.1", top_k=3)
        for r in results:
            print(engine.explain_match(r))
            print()
        assert (
            results[0]["topic_number"] == "0.1" or results[0]["doc_id"] == "doc_0"
        ), "Astrophysical doc should rank highest for galaxy query"

        # Test: Search for electroweak
        print(f"--- Test 2: Ω-search for 'quantum symmetry' ---")
        results = engine.search("electroweak symmetry quantum field", topic_hint="0.3", top_k=3)
        for r in results:
            print(f"  {r['doc_id']}: Ω-dist={r['omega_distance']:.4f}, topic={r['topic_id']}")

        # Test: Topic-based search
        print(f"\n--- Test 3: Topic search for 0.2 (planck) ---")
        results = engine.search_by_topic("0.2", top_k=3)
        for r in results:
            print(f"  {r['doc_id']}: Ω-dist={r['omega_distance']:.4f}, topic={r['topic_id']}")

        # Test: Distance components
        print(f"\n--- Test 4: Distance component analysis ---")
        vec_a = tensorizer.tensorize_text("energy conservation", topic_number="0.0")
        vec_b = tensorizer.tensorize_text("energy conservation principle", topic_number="0.0")
        vec_c = tensorizer.tensorize_text("galaxy rotation dark matter", topic_number="0.1")

        dist_ab = compute_omega_distance(vec_a, vec_b)
        dist_ac = compute_omega_distance(vec_a, vec_c)
        print(f"  Same-topic distance (a↔b): {dist_ab.combined:.4f}")
        print(f"  Cross-topic distance (a↔c): {dist_ac.combined:.4f}")
        assert dist_ab.combined <= dist_ac.combined, "Same-topic docs should have lower Ω-distance"
        print(f"  ✅ Same-topic < Cross-topic")

        print(f"\n✅ ALL TESTS PASSED")

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
