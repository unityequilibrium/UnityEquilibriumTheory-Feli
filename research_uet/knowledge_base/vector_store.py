"""
UET Hybrid Vector Store
=======================
Stores semantic embeddings + UET physics vectors side-by-side.
Supports two backends:
    1. LanceDB (recommended, pip install lancedb) — columnar, fast ANN search
    2. SQLite + JSON (zero dependencies) — portable fallback

Usage:
    from research_uet.knowledge_base.vector_store import VectorStore

    store = VectorStore("./vectors")  # auto-detects backend
    store.add(doc_id="file_001", semantic_vec=[...], uet_vec=uet_vector, metadata={...})
    results = store.search_semantic(query_vec, top_k=10)
    results = store.search_uet(query_uet_vec, top_k=10)

Rust Compatibility:
    - All data stored as JSON (serde-compatible)
    - Document schema is a flat struct with fixed fields
    - No pickle, no Python-only serialization
"""

import json
import math
import sqlite3
import time
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Optional

import numpy as np

# Try to import LanceDB
try:
    import lancedb
    import pyarrow as pa

    HAS_LANCEDB = True
except ImportError:
    HAS_LANCEDB = False


# =============================================================================
# DOCUMENT SCHEMA — Rust-compatible
# =============================================================================


@dataclass
class VectorDocument:
    """
    A document in the vector store.

    Maps directly to a Rust struct:
        #[derive(Serialize, Deserialize)]
        struct VectorDocument {
            doc_id: String,
            semantic_vec: Vec<f32>,
            uet_vec: Vec<f32>,
            ... metadata fields ...
        }
    """

    doc_id: str  # Unique identifier (file path or hash)
    semantic_vec: list[float]  # Semantic embedding (1024d from API)
    uet_vec: list[float]  # UET physics vector (20d)

    # --- Metadata ---
    topic_id: str = ""  # "0.1_Quantum_Mechanics"
    topic_number: str = ""  # "0.1"
    file_path: str = ""  # Relative path
    file_type: str = ""  # python | markdown | data
    title: str = ""  # Human-readable title
    content_hash: str = ""  # SHA-256 for dedup
    char_count: int = 0
    omega: float = 0.0  # Ω value
    kappa: float = 0.0  # κ
    beta: float = 0.0  # β
    entropy: float = 0.0  # Shannon H
    axiom_count: int = 0  # How many axioms referenced
    scale: str = ""  # Physical scale
    indexed_at: float = 0.0  # Unix timestamp

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "VectorDocument":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


@dataclass
class SearchResult:
    """Search result with score."""

    doc: VectorDocument
    score: float  # Lower = better (distance)
    match_type: str = "semantic"  # "semantic" | "uet" | "hybrid"


# =============================================================================
# VECTOR STORE — Abstract interface + implementations
# =============================================================================


class VectorStore:
    """
    Hybrid vector store for UET research data.

    Auto-selects backend:
        - LanceDB if installed (fast ANN, recommended)
        - SQLite fallback (zero deps, always works)
    """

    def __init__(self, db_path: str | Path, backend: Optional[str] = None):
        self.db_path = Path(db_path)
        self.db_path.mkdir(parents=True, exist_ok=True)

        # Select backend
        if backend == "lancedb" or (backend is None and HAS_LANCEDB):
            self._backend = _LanceDBBackend(self.db_path)
            self.backend_name = "lancedb"
        else:
            self._backend = _SQLiteBackend(self.db_path)
            self.backend_name = "sqlite"

    def add(self, doc: VectorDocument) -> None:
        """Add or update a document."""
        if doc.indexed_at == 0.0:
            doc.indexed_at = time.time()
        self._backend.upsert(doc)

    def add_batch(self, docs: list[VectorDocument]) -> int:
        """Add multiple documents. Returns count added."""
        now = time.time()
        for doc in docs:
            if doc.indexed_at == 0.0:
                doc.indexed_at = now
        return self._backend.upsert_batch(docs)

    def search_semantic(
        self,
        query_vec: list[float],
        top_k: int = 10,
    ) -> list[SearchResult]:
        """Search by semantic embedding similarity."""
        results = self._backend.search_by_vector(query_vec, "semantic_vec", top_k)
        for r in results:
            r.match_type = "semantic"
        return results

    def search_uet(
        self,
        query_uet_vec: list[float],
        top_k: int = 10,
    ) -> list[SearchResult]:
        """Search by UET physics vector similarity."""
        results = self._backend.search_by_vector(query_uet_vec, "uet_vec", top_k)
        for r in results:
            r.match_type = "uet"
        return results

    def search_hybrid(
        self,
        semantic_vec: list[float],
        uet_vec: list[float],
        top_k: int = 10,
        uet_weight: float = 0.3,
    ) -> list[SearchResult]:
        """
        Hybrid search: combine semantic + UET physics results.

        Args:
            semantic_vec: Semantic query embedding
            uet_vec: UET physics query vector
            top_k: Number of results
            uet_weight: Weight for UET score (0=semantic only, 1=UET only)
        """
        # Get candidates from both
        sem_results = self.search_semantic(semantic_vec, top_k=top_k * 2)
        uet_results = self.search_uet(uet_vec, top_k=top_k * 2)

        # Merge by doc_id with weighted scores
        scores: dict[str, dict] = {}

        for r in sem_results:
            scores[r.doc.doc_id] = {
                "doc": r.doc,
                "sem_score": r.score,
                "uet_score": float("inf"),
            }

        for r in uet_results:
            if r.doc.doc_id in scores:
                scores[r.doc.doc_id]["uet_score"] = r.score
            else:
                scores[r.doc.doc_id] = {
                    "doc": r.doc,
                    "sem_score": float("inf"),
                    "uet_score": r.score,
                }

        # Normalize scores (min-max per column)
        all_entries = list(scores.values())
        if not all_entries:
            return []

        sem_vals = [e["sem_score"] for e in all_entries if e["sem_score"] != float("inf")]
        uet_vals = [e["uet_score"] for e in all_entries if e["uet_score"] != float("inf")]

        sem_min = min(sem_vals) if sem_vals else 0
        sem_max = max(sem_vals) if sem_vals else 1
        uet_min = min(uet_vals) if uet_vals else 0
        uet_max = max(uet_vals) if uet_vals else 1

        sem_range = max(sem_max - sem_min, 1e-9)
        uet_range = max(uet_max - uet_min, 1e-9)

        # Compute hybrid score
        results = []
        for e in all_entries:
            sem_norm = (
                (e["sem_score"] - sem_min) / sem_range if e["sem_score"] != float("inf") else 1.0
            )
            uet_norm = (
                (e["uet_score"] - uet_min) / uet_range if e["uet_score"] != float("inf") else 1.0
            )
            hybrid = (1 - uet_weight) * sem_norm + uet_weight * uet_norm
            results.append(SearchResult(doc=e["doc"], score=hybrid, match_type="hybrid"))

        results.sort(key=lambda r: r.score)
        return results[:top_k]

    def get(self, doc_id: str) -> Optional[VectorDocument]:
        """Get a document by ID."""
        return self._backend.get(doc_id)

    def delete(self, doc_id: str) -> bool:
        """Delete a document by ID."""
        return self._backend.delete(doc_id)

    def count(self) -> int:
        """Total number of documents."""
        return self._backend.count()

    def list_topics(self) -> list[str]:
        """List all unique topic_ids."""
        return self._backend.list_topics()

    def stats(self) -> dict:
        """Get store statistics."""
        return {
            "backend": self.backend_name,
            "total_docs": self.count(),
            "db_path": str(self.db_path),
            "topics": self.list_topics(),
        }


# =============================================================================
# LANCEDB BACKEND
# =============================================================================


class _LanceDBBackend:
    """LanceDB backend — fast ANN search with Apache Arrow."""

    TABLE_NAME = "uet_vectors"

    def __init__(self, db_path: Path):
        self.db = lancedb.connect(str(db_path / "lance"))
        self._ensure_table()

    def _ensure_table(self):
        """Create table if not exists."""
        if self.TABLE_NAME not in self.db.table_names():
            # Create with empty schema
            self._table = None
        else:
            self._table = self.db.open_table(self.TABLE_NAME)

    def upsert(self, doc: VectorDocument):
        data = doc.to_dict()
        if self._table is None:
            self._table = self.db.create_table(self.TABLE_NAME, [data])
        else:
            # Delete existing if present, then add
            try:
                self._table.delete(f'doc_id = "{doc.doc_id}"')
            except Exception:
                pass
            self._table.add([data])

    def upsert_batch(self, docs: list[VectorDocument]) -> int:
        data = [d.to_dict() for d in docs]
        if self._table is None:
            self._table = self.db.create_table(self.TABLE_NAME, data)
        else:
            # Delete existing docs
            for doc in docs:
                try:
                    self._table.delete(f'doc_id = "{doc.doc_id}"')
                except Exception:
                    pass
            self._table.add(data)
        return len(data)

    def search_by_vector(
        self, query_vec: list[float], vec_field: str, top_k: int
    ) -> list[SearchResult]:
        if self._table is None:
            return []

        results = self._table.search(query_vec, vector_column_name=vec_field).limit(top_k).to_list()

        return [
            SearchResult(
                doc=VectorDocument.from_dict(r),
                score=r.get("_distance", 0.0),
            )
            for r in results
        ]

    def get(self, doc_id: str) -> Optional[VectorDocument]:
        if self._table is None:
            return None
        results = self._table.search().where(f'doc_id = "{doc_id}"').limit(1).to_list()
        return VectorDocument.from_dict(results[0]) if results else None

    def delete(self, doc_id: str) -> bool:
        if self._table is None:
            return False
        try:
            self._table.delete(f'doc_id = "{doc_id}"')
            return True
        except Exception:
            return False

    def count(self) -> int:
        if self._table is None:
            return 0
        return self._table.count_rows()

    def list_topics(self) -> list[str]:
        if self._table is None:
            return []
        df = self._table.to_pandas()
        return sorted(df["topic_id"].unique().tolist()) if "topic_id" in df.columns else []


# =============================================================================
# SQLITE BACKEND (Zero-dependency fallback)
# =============================================================================


class _SQLiteBackend:
    """SQLite + JSON backend — works everywhere, no extra deps."""

    def __init__(self, db_path: Path):
        self.db_file = db_path / "vectors.db"
        self._conn = sqlite3.connect(str(self.db_file))
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._create_tables()

    def _create_tables(self):
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                doc_id TEXT PRIMARY KEY,
                semantic_vec TEXT,
                uet_vec TEXT,
                topic_id TEXT,
                topic_number TEXT,
                file_path TEXT,
                file_type TEXT,
                title TEXT,
                content_hash TEXT,
                char_count INTEGER,
                omega REAL,
                kappa REAL,
                beta REAL,
                entropy REAL,
                axiom_count INTEGER,
                scale TEXT,
                indexed_at REAL
            )
        """
        )
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_topic ON documents(topic_id)")
        self._conn.execute("CREATE INDEX IF NOT EXISTS idx_hash ON documents(content_hash)")
        self._conn.commit()

    def upsert(self, doc: VectorDocument):
        d = doc.to_dict()
        d["semantic_vec"] = json.dumps(d["semantic_vec"])
        d["uet_vec"] = json.dumps(d["uet_vec"])

        cols = ", ".join(d.keys())
        placeholders = ", ".join(["?"] * len(d))
        self._conn.execute(
            f"INSERT OR REPLACE INTO documents ({cols}) VALUES ({placeholders})",
            list(d.values()),
        )
        self._conn.commit()

    def upsert_batch(self, docs: list[VectorDocument]) -> int:
        for doc in docs:
            self.upsert(doc)
        return len(docs)

    def search_by_vector(
        self, query_vec: list[float], vec_field: str, top_k: int
    ) -> list[SearchResult]:
        """Brute-force cosine distance search (fine for < 50K docs)."""
        cursor = self._conn.execute(f"SELECT * FROM documents")
        columns = [desc[0] for desc in cursor.description]

        query_arr = np.array(query_vec, dtype=np.float32)
        query_norm = np.linalg.norm(query_arr)
        if query_norm == 0:
            return []

        scored = []
        for row in cursor:
            row_dict = dict(zip(columns, row))
            # Parse stored vector
            stored_vec = json.loads(row_dict[vec_field])
            stored_arr = np.array(stored_vec, dtype=np.float32)

            stored_norm = np.linalg.norm(stored_arr)
            if stored_norm == 0:
                continue

            # Cosine distance (0 = identical, 2 = opposite)
            cosine_sim = np.dot(query_arr, stored_arr) / (query_norm * stored_norm)
            distance = 1.0 - float(cosine_sim)

            # Reconstruct document
            row_dict["semantic_vec"] = json.loads(row_dict["semantic_vec"])
            row_dict["uet_vec"] = json.loads(row_dict["uet_vec"])
            doc = VectorDocument.from_dict(row_dict)

            scored.append(SearchResult(doc=doc, score=distance))

        # Sort by distance (ascending = most similar first)
        scored.sort(key=lambda r: r.score)
        return scored[:top_k]

    def get(self, doc_id: str) -> Optional[VectorDocument]:
        cursor = self._conn.execute("SELECT * FROM documents WHERE doc_id = ?", (doc_id,))
        columns = [desc[0] for desc in cursor.description]
        row = cursor.fetchone()
        if not row:
            return None
        d = dict(zip(columns, row))
        d["semantic_vec"] = json.loads(d["semantic_vec"])
        d["uet_vec"] = json.loads(d["uet_vec"])
        return VectorDocument.from_dict(d)

    def delete(self, doc_id: str) -> bool:
        cursor = self._conn.execute("DELETE FROM documents WHERE doc_id = ?", (doc_id,))
        self._conn.commit()
        return cursor.rowcount > 0

    def count(self) -> int:
        cursor = self._conn.execute("SELECT COUNT(*) FROM documents")
        return cursor.fetchone()[0]

    def list_topics(self) -> list[str]:
        cursor = self._conn.execute("SELECT DISTINCT topic_id FROM documents ORDER BY topic_id")
        return [row[0] for row in cursor if row[0]]


# =============================================================================
# STANDALONE TEST
# =============================================================================

if __name__ == "__main__":
    import tempfile
    import shutil

    print("=" * 60)
    print(f"  UET Vector Store — Self Test")
    print(f"  Backend: {'LanceDB' if HAS_LANCEDB else 'SQLite (fallback)'}")
    print("=" * 60)

    # Create temp directory
    tmp_dir = Path(tempfile.mkdtemp(prefix="uet_vstore_"))

    try:
        store = VectorStore(tmp_dir)
        print(f"\n  Backend selected: {store.backend_name}")

        # Create test documents
        docs = []
        for i in range(5):
            doc = VectorDocument(
                doc_id=f"test_{i}",
                semantic_vec=[float(x) for x in np.random.randn(8)],  # Small for test
                uet_vec=[float(x) for x in np.random.randn(20)],
                topic_id=f"0.{i}_TestTopic",
                topic_number=f"0.{i}",
                file_path=f"topics/0.{i}_Test/Research.py",
                file_type="python",
                title=f"Test Document {i}",
                content_hash=f"hash_{i}",
                char_count=1000 * (i + 1),
                omega=0.1 * (i + 1),
                kappa=0.1,
                beta=0.05 * (i + 1),
                entropy=4.0 + i * 0.2,
                axiom_count=i + 3,
                scale="general",
            )
            docs.append(doc)

        # Test: Add batch
        print("\n--- Test 1: Batch insert ---")
        count = store.add_batch(docs)
        print(f"  Added {count} documents")
        assert store.count() == 5, f"Expected 5, got {store.count()}"
        print(f"  Total documents: {store.count()}")

        # Test: Get by ID
        print("\n--- Test 2: Get by ID ---")
        doc = store.get("test_2")
        assert doc is not None
        assert doc.topic_id == "0.2_TestTopic"
        print(f"  Got: {doc.doc_id} → {doc.topic_id} (Ω={doc.omega})")

        # Test: Semantic search
        print("\n--- Test 3: Semantic search ---")
        query = docs[0].semantic_vec  # Search for doc_0's vector
        results = store.search_semantic(query, top_k=3)
        print(f"  Top 3 results:")
        for r in results:
            print(f"    {r.doc.doc_id} → score={r.score:.4f} ({r.match_type})")
        assert results[0].doc.doc_id == "test_0", "First result should be exact match"

        # Test: UET search
        print("\n--- Test 4: UET physics search ---")
        query_uet = docs[3].uet_vec
        results = store.search_uet(query_uet, top_k=3)
        print(f"  Top 3 results:")
        for r in results:
            print(f"    {r.doc.doc_id} → score={r.score:.4f} ({r.match_type})")
        assert results[0].doc.doc_id == "test_3"

        # Test: Hybrid search
        print("\n--- Test 5: Hybrid search ---")
        results = store.search_hybrid(
            semantic_vec=docs[1].semantic_vec,
            uet_vec=docs[1].uet_vec,
            top_k=3,
            uet_weight=0.3,
        )
        print(f"  Top 3 results (uet_weight=0.3):")
        for r in results:
            print(f"    {r.doc.doc_id} → score={r.score:.4f} ({r.match_type})")
        assert results[0].doc.doc_id == "test_1"

        # Test: Delete
        print("\n--- Test 6: Delete ---")
        deleted = store.delete("test_4")
        assert deleted
        assert store.count() == 4
        print(f"  Deleted test_4 → count={store.count()}")

        # Test: Dedup (upsert same ID)
        print("\n--- Test 7: Upsert dedup ---")
        updated_doc = docs[0]
        updated_doc.title = "Updated Title"
        store.add(updated_doc)
        assert store.count() == 4, "Count should stay 4 after upsert"
        retrieved = store.get("test_0")
        assert retrieved.title == "Updated Title"
        print(f"  Upserted test_0 → title='{retrieved.title}', count={store.count()}")

        # Test: Topics
        print("\n--- Test 8: List topics ---")
        topics = store.list_topics()
        print(f"  Topics: {topics}")

        # Test: Stats
        print("\n--- Test 9: Stats ---")
        stats = store.stats()
        for k, v in stats.items():
            print(f"  {k}: {v}")

        print("\n✅ ALL TESTS PASSED")

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
