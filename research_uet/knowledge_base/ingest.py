"""
UET Ingestion Pipeline
======================
Scan → Tensorize → Store — bulk pipeline for research_uet/topics/

Processes the entire research corpus:
    1. Walk topics/ directory (9K+ files)
    2. Filter by type (.py, .md, .json, .csv)
    3. Tensorize each file → UetVector (physics metrics)
    4. Store in VectorStore (semantic + UET vectors)

Supports:
    - Dry-run mode (scan only, no writes)
    - Incremental ingestion (skip already-indexed files via content_hash)
    - Progress reporting
    - File chunking for large documents (>10K chars)

Usage:
    # Dry-run:
    python -m research_uet.knowledge_base.ingest --dry-run

    # Full ingestion:
    python -m research_uet.knowledge_base.ingest

    # Single topic:
    python -m research_uet.knowledge_base.ingest --topic 0.0_Grand_Unification

Rust Compatibility:
    - All file metadata is JSON-serializable
    - No Python-specific serialization (no pickle)
"""

import hashlib
import json
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .tensorizer import UetTensorizer, UetVector
from .vector_store import VectorStore, VectorDocument
from .api_client import OpenRouterClient, CostTracker


# =============================================================================
# CONFIGURATION
# =============================================================================

# File types to process
SUPPORTED_EXTENSIONS = {".py", ".md", ".txt", ".json", ".csv", ".toml", ".yaml", ".yml"}

# Skip patterns (directories and files)
SKIP_DIRS = {"__pycache__", ".git", ".venv", "node_modules", ".mypy_cache", "vectors"}
SKIP_FILES = {"__init__.py"}  # Usually empty or trivial

# Chunking
MAX_CHUNK_CHARS = 8000  # Split files larger than this
CHUNK_OVERLAP = 200  # Characters overlap between chunks

# Topic pattern: "0.1_Quantum_Mechanics" → topic_number="0.1"
TOPIC_PATTERN = re.compile(r"^(\d+\.\d+)_(.+)$")


# =============================================================================
# DATA CLASSES
# =============================================================================


@dataclass
class IngestStats:
    """Statistics for an ingestion run."""

    files_scanned: int = 0
    files_indexed: int = 0
    files_skipped: int = 0  # Already indexed (same hash)
    files_errored: int = 0
    chunks_created: int = 0
    topics_processed: int = 0
    total_chars: int = 0
    total_bytes: int = 0
    elapsed_seconds: float = 0.0
    errors: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "files_scanned": self.files_scanned,
            "files_indexed": self.files_indexed,
            "files_skipped": self.files_skipped,
            "files_errored": self.files_errored,
            "chunks_created": self.chunks_created,
            "topics_processed": self.topics_processed,
            "total_chars": self.total_chars,
            "total_bytes": self.total_bytes,
            "elapsed_seconds": round(self.elapsed_seconds, 2),
            "errors": self.errors[:10],  # Cap at 10
        }

    def summary(self) -> str:
        lines = [
            "=" * 60,
            "  Ingestion Report",
            "=" * 60,
            f"  Topics processed:  {self.topics_processed}",
            f"  Files scanned:     {self.files_scanned}",
            f"  Files indexed:     {self.files_indexed}",
            f"  Files skipped:     {self.files_skipped} (already indexed)",
            f"  Files errored:     {self.files_errored}",
            f"  Chunks created:    {self.chunks_created}",
            f"  Total chars:       {self.total_chars:,}",
            f"  Total bytes:       {self.total_bytes:,}",
            f"  Elapsed:           {self.elapsed_seconds:.1f}s",
        ]
        if self.errors:
            lines.append(f"\n  First {min(len(self.errors), 5)} errors:")
            for err in self.errors[:5]:
                lines.append(f"    ❌ {err['file']}: {err['error']}")
        return "\n".join(lines)


# =============================================================================
# INGESTION PIPELINE
# =============================================================================


class IngestionPipeline:
    """
    Bulk ingestion pipeline for UET research files.

    Scans research_uet/topics/ → tensorizes each file → stores in VectorStore.
    """

    def __init__(
        self,
        store: VectorStore,
        tensorizer: UetTensorizer,
        api_client: Optional[OpenRouterClient] = None,
        topics_dir: Optional[Path] = None,
    ):
        self.store = store
        self.tensorizer = tensorizer
        self.api_client = api_client

        # Default topics directory
        if topics_dir is None:
            self.topics_dir = Path(__file__).resolve().parent.parent / "topics"
        else:
            self.topics_dir = Path(topics_dir)

    def ingest_all(self, dry_run: bool = False, force: bool = False) -> IngestStats:
        """
        Ingest all topics.

        Args:
            dry_run: If True, scan and report but don't store

        Returns:
            IngestStats with full report
        """
        stats = IngestStats()
        start = time.time()

        if not self.topics_dir.exists():
            print(f"  ❌ Topics directory not found: {self.topics_dir}")
            return stats

        # Find topic directories
        topic_dirs = sorted(
            [d for d in self.topics_dir.iterdir() if d.is_dir() and TOPIC_PATTERN.match(d.name)]
        )

        print(f"  Found {len(topic_dirs)} topic directories")
        if dry_run:
            print("  🔍 DRY RUN — scanning only, no writes\n")

        for topic_dir in topic_dirs:
            topic_stats = self.ingest_topic(topic_dir, dry_run=dry_run, force=force)
            stats.files_scanned += topic_stats.files_scanned
            stats.files_indexed += topic_stats.files_indexed
            stats.files_skipped += topic_stats.files_skipped
            stats.files_errored += topic_stats.files_errored
            stats.chunks_created += topic_stats.chunks_created
            stats.total_chars += topic_stats.total_chars
            stats.total_bytes += topic_stats.total_bytes
            stats.errors.extend(topic_stats.errors)
            stats.topics_processed += 1

        stats.elapsed_seconds = time.time() - start
        return stats

    def ingest_topic(
        self,
        topic_dir: Path,
        dry_run: bool = False,
        force: bool = False,
    ) -> IngestStats:
        """
        Ingest a single topic directory.

        Args:
            topic_dir: Path to topic directory (e.g. topics/0.1_Astrophysics/)
            dry_run: Scan only
        """
        stats = IngestStats()

        # Parse topic info
        match = TOPIC_PATTERN.match(topic_dir.name)
        if match:
            topic_number = match.group(1)
            topic_name = match.group(2)
            topic_id = topic_dir.name
        else:
            topic_number = "0.0"
            topic_name = topic_dir.name
            topic_id = topic_dir.name

        # Collect eligible files
        files = self._collect_files(topic_dir)
        stats.files_scanned = len(files)

        if files:
            print(f"  📂 {topic_id}: {len(files)} files", end="")

        for filepath in files:
            try:
                result = self._process_file(filepath, topic_id, topic_number, dry_run, force)
                if result == "indexed":
                    stats.files_indexed += 1
                    stats.total_chars += filepath.stat().st_size  # Approximate
                    stats.total_bytes += filepath.stat().st_size
                elif result == "skipped":
                    stats.files_skipped += 1
                elif result == "chunked":
                    # Count chunks
                    content = filepath.read_text(encoding="utf-8", errors="replace")
                    n_chunks = max(1, len(content) // (MAX_CHUNK_CHARS - CHUNK_OVERLAP))
                    stats.chunks_created += n_chunks
                    stats.files_indexed += 1
                    stats.total_chars += len(content)
                    stats.total_bytes += filepath.stat().st_size
            except Exception as e:
                stats.files_errored += 1
                stats.errors.append(
                    {
                        "file": str(filepath.relative_to(self.topics_dir)),
                        "error": str(e)[:200],
                    }
                )

        if files:
            status = "📊" if dry_run else "✅"
            print(
                f" → {status} {stats.files_indexed} indexed, "
                f"{stats.files_skipped} skipped, "
                f"{stats.files_errored} errors"
            )

        stats.topics_processed = 1
        return stats

    def _collect_files(self, directory: Path) -> list[Path]:
        """Recursively collect eligible files from a directory."""
        files = []
        for item in sorted(directory.rglob("*")):
            # Skip directories in skip list
            if any(skip in item.parts for skip in SKIP_DIRS):
                continue
            if not item.is_file():
                continue
            if item.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            if item.name in SKIP_FILES:
                continue
            # Skip very small files (<50 bytes, likely empty)
            if item.stat().st_size < 50:
                continue
            files.append(item)
        return files

    def _process_file(
        self,
        filepath: Path,
        topic_id: str,
        topic_number: str,
        dry_run: bool,
        force: bool = False,
    ) -> str:
        """
        Process a single file.

        Returns: "indexed", "skipped", or "chunked"
        """
        # Read content
        content = filepath.read_text(encoding="utf-8", errors="replace")

        # Compute content hash for dedup
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]

        # Check if already indexed
        doc_id = self._make_doc_id(filepath)
        existing = self.store.get(doc_id)
        if not force and existing and existing.content_hash == content_hash:
            return "skipped"

        if dry_run:
            return "indexed"  # Would index

        # Determine file type
        file_type = self._classify_file(filepath)

        # Check if chunking needed
        if len(content) > MAX_CHUNK_CHARS:
            self._process_chunked(
                filepath, content, topic_id, topic_number, file_type, content_hash
            )
            return "chunked"

        # Tensorize
        uet_vec = self.tensorizer.tensorize_text(
            content, topic_number=topic_number, label=filepath.name
        )

        # Generate embedding if client available
        semantic_vec = [0.0] * 8
        if self.api_client and not dry_run:
            try:
                # Use first 1000 chars for embedding to save costs/tokens if needed
                # or just embed the whole thing if the model supports it.
                # qwen-embedding-8b supports 32k context, so full text is fine.
                vectors = self.api_client.embed([content[:8000]])
                if vectors:
                    semantic_vec = vectors[0]
            except Exception as e:
                print(f"  ⚠️ Embedding failed for {filepath.name}: {e}")

        # Create document
        doc = VectorDocument(
            doc_id=doc_id,
            semantic_vec=semantic_vec,
            uet_vec=uet_vec.to_flat_vector(),
            text=content,  # Store full text
            topic_id=topic_id,
            topic_number=topic_number,
            file_path=str(filepath.relative_to(self.topics_dir)),
            file_type=file_type,
            title=self._extract_title(filepath, content),
            content_hash=content_hash,
            char_count=len(content),
            omega=uet_vec.omega,
            kappa=uet_vec.kappa,
            beta=uet_vec.beta,
            entropy=uet_vec.entropy,
            axiom_count=uet_vec.axiom_count,
            axiom_signature=json.dumps(uet_vec.axiom_signature),
            scale=uet_vec.scale,
        )

        self.store.add(doc)
        return "indexed"

    def _process_chunked(
        self,
        filepath: Path,
        content: str,
        topic_id: str,
        topic_number: str,
        file_type: str,
        content_hash: str,
    ):
        """Process a large file by splitting into chunks."""
        chunks = self._split_chunks(content)

        for i, chunk in enumerate(chunks):
            chunk_id = f"{self._make_doc_id(filepath)}__chunk_{i}"

            uet_vec = self.tensorizer.tensorize_text(
                chunk, topic_number=topic_number, label=f"{filepath.name}[{i}]"
            )

            # Generate embedding for chunk
            semantic_vec = [0.0] * 8
            if self.api_client:
                try:
                    vectors = self.api_client.embed([chunk])
                    if vectors:
                        semantic_vec = vectors[0]
                except Exception:
                    pass

            doc = VectorDocument(
                doc_id=chunk_id,
                semantic_vec=semantic_vec,
                uet_vec=uet_vec.to_flat_vector(),
                text=chunk,  # Store chunk text
                topic_id=topic_id,
                topic_number=topic_number,
                file_path=str(filepath.relative_to(self.topics_dir)),
                file_type=file_type,
                title=f"{self._extract_title(filepath, content)} [chunk {i+1}/{len(chunks)}]",
                content_hash=f"{content_hash}_c{i}",
                char_count=len(chunk),
                omega=uet_vec.omega,
                kappa=uet_vec.kappa,
                beta=uet_vec.beta,
                entropy=uet_vec.entropy,
                axiom_count=uet_vec.axiom_count,
                axiom_signature=json.dumps(uet_vec.axiom_signature),
                scale=uet_vec.scale,
            )
            self.store.add(doc)

    def _split_chunks(self, content: str) -> list[str]:
        """Split content into overlapping chunks."""
        chunks = []
        start = 0
        while start < len(content):
            end = start + MAX_CHUNK_CHARS

            # Try to break at a paragraph boundary
            if end < len(content):
                # Look for double newline near the end
                break_pos = content.rfind("\n\n", start + MAX_CHUNK_CHARS // 2, end)
                if break_pos > start:
                    end = break_pos + 2  # Include the newlines

            chunks.append(content[start:end])
            start = end - CHUNK_OVERLAP

        return chunks

    def _make_doc_id(self, filepath: Path) -> str:
        """Create a stable document ID from filepath."""
        try:
            rel = filepath.relative_to(self.topics_dir)
        except ValueError:
            rel = filepath
        # Normalize path separators
        return str(rel).replace("\\", "/")

    def _classify_file(self, filepath: Path) -> str:
        """Classify file type."""
        ext = filepath.suffix.lower()
        if ext == ".py":
            return "python"
        elif ext == ".md":
            return "markdown"
        elif ext in {".json", ".csv", ".toml", ".yaml", ".yml"}:
            return "data"
        elif ext == ".txt":
            return "text"
        return "other"

    def _extract_title(self, filepath: Path, content: str) -> str:
        """Extract a title from file content or name."""
        # Try to find a title in the content
        for line in content.split("\n")[:10]:
            line = line.strip()
            # Markdown header
            if line.startswith("# ") and len(line) > 3:
                return line[2:].strip()[:100]
            # Python docstring first line
            if line.startswith('"""') or line.startswith("'''"):
                title = line.strip("\"' ")
                if title and len(title) > 3:
                    return title[:100]

        # Fallback to filename
        return filepath.stem.replace("_", " ").title()


# =============================================================================
# CLI INTERFACE
# =============================================================================


def main():
    """CLI entry point."""
    import argparse
    import sys

    # Find project root
    project_root = Path(__file__).resolve().parent.parent.parent

    parser = argparse.ArgumentParser(description="UET Ingestion Pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Scan only, no writes")
    parser.add_argument(
        "--topic", type=str, help="Ingest single topic (e.g. 0.0_Grand_Unification)"
    )
    parser.add_argument(
        "--db-path",
        type=str,
        default=str(project_root / "research_uet" / "knowledge_base" / "vectors"),
        help="Vector store path",
    )
    parser.add_argument("--force", action="store_true", help="Re-index existing files")
    parser.add_argument("--embed", action="store_true", help="Generate embeddings via API")
    args = parser.parse_args()

    print("=" * 60)
    print("  UET Ingestion Pipeline")
    print("=" * 60)

    # Initialize components
    store = VectorStore(args.db_path)
    tensorizer = UetTensorizer(grid_size=64)

    api_client = None
    if args.embed:
        from .config import CONFIG

        client_config = CONFIG["openrouter"]
        # Use embeddings key if available, else default
        keys = client_config.get("keys", {})
        key = keys.get("embedding") or keys.get("default")

        if not key or "CHANGEME" in key:
            print("  ⚠️ No valid API key found for embeddings. Skipping API init.")
        else:
            api_client = OpenRouterClient(
                base_url=client_config["base_url"],
                keys=keys,
                agents=CONFIG["agents"],
                cost_tracker=CostTracker(Path(CONFIG["cost_tracking"]["log_file"])),
            )
            print("  ✅ API Client initialized for embeddings")

    pipeline = IngestionPipeline(store, tensorizer, api_client=api_client)

    print(f"  Store: {store.backend_name} @ {args.db_path}")
    print(f"  Topics: {pipeline.topics_dir}")
    print(f"  Existing docs: {store.count()}\n")

    if args.topic:
        # Single topic
        topic_dir = pipeline.topics_dir / args.topic
        if not topic_dir.exists():
            print(f"  ❌ Topic not found: {topic_dir}")
            sys.exit(1)
        stats = pipeline.ingest_topic(topic_dir, dry_run=args.dry_run, force=args.force)
    else:
        # All topics
        stats = pipeline.ingest_all(dry_run=args.dry_run, force=args.force)

    print(f"\n{stats.summary()}")
    print(f"\n  Store now has: {store.count()} documents")

    if args.dry_run:
        print("\n  ℹ️  This was a DRY RUN — no data was written")


if __name__ == "__main__":
    main()
