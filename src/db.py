import duckdb

DB_PATH = "data/placements.duckdb"

def get_connection():
    """Create and return a DuckDB connection."""
    return duckdb.connect(DB_PATH)

def init_db():
    """Initialize the placements table schema if it does not exist."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS placements (
            id INTEGER PRIMARY KEY,
            company VARCHAR,
            role VARCHAR,
            location VARCHAR,
            salary_gbp INTEGER
        )
    """)
    conn.close()
    print("[INFO] DuckDB Schema initialized successfully.")

if __name__ == "__main__":
    init_db()