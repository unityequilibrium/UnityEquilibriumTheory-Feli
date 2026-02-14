import sqlite3
import psycopg2
import uuid
import json
from pathlib import Path
from tqdm import tqdm
from datetime import datetime

# Configuration
SQLITE_DB_PATH = Path("research_uet/knowledge_base/vectors/vectors.db")
POSTGRES_DSN = "host=localhost port=5433 dbname=uet_kb user=postgres password=postgres"


def migrate():
    print(f"Connecting to SQLite at {SQLITE_DB_PATH}...")
    try:
        lite_conn = sqlite3.connect(SQLITE_DB_PATH)
        lite_cur = lite_conn.cursor()
    except Exception as e:
        print(f"Error connecting to SQLite: {e}")
        return

    print("Fetching records count...")
    lite_cur.execute("SELECT COUNT(*) FROM documents")
    total_records = lite_cur.fetchone()[0]
    print(f"Found {total_records} records to migrate.")

    # Connect to Postgres
    print(f"Connecting to Postgres at {POSTGRES_DSN}...")
    try:
        pg_conn = psycopg2.connect(POSTGRES_DSN)
        pg_cur = pg_conn.cursor()
    except Exception as e:
        print(f"Error connecting to Postgres: {e}")
        return

    # Map file_path -> doc_uuid to avoid duplicate documents
    path_to_uuid = {}

    print("Starting migration...")

    # Track stats
    docs_inserted = 0
    chunks_inserted = 0

    # We'll use a transaction
    try:
        # Fetch all rows from SQLite
        # Columns in SQLite: doc_id, semantic_vec, uet_vec, text, topic_id, topic_number, file_path, ...
        lite_cur.execute("SELECT doc_id, semantic_vec, uet_vec, text, file_path FROM documents")

        for row in tqdm(lite_cur, total=total_records, desc="Migrating records"):
            lite_doc_id, sem_vec_str, uet_vec_str, text, file_path = row

            if not file_path:
                file_path = "unknown"

            # 1. Handle Document
            if file_path not in path_to_uuid:
                doc_uuid = str(uuid.uuid4())
                path_to_uuid[file_path] = doc_uuid

                pg_cur.execute(
                    "INSERT INTO documents (id, path, extracted_text, created_at) VALUES (%s, %s, %s, %s)",
                    (doc_uuid, file_path, "", datetime.now().isoformat()),
                )
                docs_inserted += 1

            doc_uuid = path_to_uuid[file_path]

            # 2. Handle Chunk
            chunk_pub_id = str(uuid.uuid4())

            # Sanitize text
            if text:
                text = text.replace("\x00", "")

            # Convert vectors to lists of floats
            try:
                # SQLite stores vectors as strings like "[1, 2, ...]"
                semantic_vec = json.loads(sem_vec_str)
                physics_vec = json.loads(uet_vec_str)

                # Zero-pad semantic vector to 1024 dimensions if needed
                if len(semantic_vec) < 1024:
                    semantic_vec.extend([0.0] * (1024 - len(semantic_vec)))
                elif len(semantic_vec) > 1024:
                    semantic_vec = semantic_vec[:1024]

                # pgvector expects string format "[0.1, 0.2, ...]"
                sem_vec_pg = "[" + ",".join(map(str, semantic_vec)) + "]"
                phys_vec_pg = "[" + ",".join(map(str, physics_vec)) + "]"

            except Exception as e:
                print(f"Error parsing vectors for {lite_doc_id}: {e}")
                continue

            pg_cur.execute(
                "INSERT INTO chunks (id, doc_id, text, embedding, physics_vector) VALUES (%s, %s, %s, %s::vector, %s::vector)",
                (chunk_pub_id, doc_uuid, text, sem_vec_pg, phys_vec_pg),
            )
            chunks_inserted += 1

            # Commit every 500 records
            if chunks_inserted % 500 == 0:
                pg_conn.commit()

        pg_conn.commit()
        print(f"\nMigration complete!")
        print(f"Documents created: {docs_inserted}")
        print(f"Chunks migrated: {chunks_inserted}")

    except Exception as e:
        pg_conn.rollback()
        print(f"Error during migration: {e}")
    finally:
        lite_conn.close()
        pg_cur.close()
        pg_conn.close()


if __name__ == "__main__":
    migrate()
