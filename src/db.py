import duckdb
import pandas as pd

DB_PATH = "data/placements.duckdb"

def get_connection():
    """Create and return a DuckDB connection."""
    return duckdb.connect(DB_PATH)

def init_db():
    """Initialize the database schema and seed diverse initial sample data."""
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
    
    # Check if table is empty
    result = conn.execute("SELECT COUNT(*) FROM placements").fetchone()
    if result[0] == 0:
        # Seed extended UK tech placement listings
        conn.execute("""
            INSERT INTO placements VALUES
            (1, 'Google', 'Software Engineer Intern', 'London', 45000),
            (2, 'Amazon', 'Data Analyst Intern', 'London', 40000),
            (3, 'Revolut', 'Backend Developer Intern', 'London', 42000),
            (4, 'Arm', 'Embedded Systems Engineer Intern', 'Cambridge', 38000),
            (5, 'Barclays', 'Cybersecurity Intern', 'Northwich', 32000),
            (6, 'Arup', 'Data Scientist Intern', 'Manchester', 34000),
            (7, 'BT Group', 'Software Developer Intern', 'Belfast', 31000),
            (8, 'Skyscanner', 'Frontend Engineer Intern', 'Edinburgh', 36000),
            (9, 'Monzo', 'Mobile Developer Intern', 'London', 43000),
            (10, 'BAE Systems', 'AI & ML Engineer Intern', 'Leeds', 35000)
        """)
        print("[SUCCESS] Extended sample data initialized successfully.")
    else:
        print("[INFO] Database table already exists.")
        
    conn.close()

def reset_and_reseed_db():
    """Drop existing table and re-initialize with new expanded data."""
    conn = get_connection()
    conn.execute("DROP TABLE IF EXISTS placements")
    conn.close()
    init_db()

if __name__ == "__main__":
    reset_and_reseed_db()