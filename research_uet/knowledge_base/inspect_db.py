import sqlite3
import json


def inspect():
    db_path = "research_uet/knowledge_base/vectors/vectors.db"
    print(f"Inspecting {db_path}...")
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # List tables
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cur.fetchall()
        print(f"Tables: {tables}")

        for table_name in [t[0] for t in tables]:
            print(f"\n--- Table: {table_name} ---")
            cur.execute(f"PRAGMA table_info({table_name})")
            print(f"Columns: {cur.fetchall()}")

            cur.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cur.fetchone()[0]
            print(f"Row count: {count}")

            if count > 0:
                cur.execute(f"SELECT * FROM {table_name} LIMIT 1")
                print(f"Sample row: {cur.fetchone()}")

        conn.close()
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    inspect()
