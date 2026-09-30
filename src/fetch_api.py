import os
from dotenv import load_dotenv
import requests
import duckdb
from src.db import get_connection

load_dotenv()

# Adzuna API
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
BASE_URL = "https://api.adzuna.com/v1/api/jobs/gb/search"

def fetch_uk_tech_jobs(pages=3, results_per_page=50):
    """
    Fetch live tech placement & internship jobs across the UK from Adzuna API.
    Supports multi-page fetching to increase dataset size.
    """
    all_jobs = []
    
    for page in range(1, pages + 1):
        url = f"{BASE_URL}/{page}"
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": results_per_page,
            "what": "developer", 
            "content-type": "application/json"
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            print(f"[DEBUG] Fetching Page {page} - Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                jobs = data.get("results", [])
                all_jobs.extend(jobs)
                print(f"[INFO] Fetched {len(jobs)} jobs from Page {page}.")
            else:
                print(f"[WARNING] Page {page} request failed: {response.text}")
                
        except Exception as e:
            print(f"[ERROR] Exception occurred on Page {page}: {e}")
            
    return all_jobs

def sync_api_to_db():
    """Extract, transform, and load multi-page job records into DuckDB."""
    # Fetch 3 pages, 50 results per page (up to 150 jobs)
    jobs = fetch_uk_tech_jobs(pages=3, results_per_page=50)
    if not jobs:
        print("[WARNING] No jobs fetched or API request failed.")
        return

    conn = get_connection()
    
    # Ensure database table schema exists
    conn.execute("""
        CREATE TABLE IF NOT EXISTS placements (
            id INTEGER PRIMARY KEY,
            company VARCHAR,
            role VARCHAR,
            location VARCHAR,
            salary_gbp INTEGER
        )
    """)
    
    current_max = conn.execute("SELECT COALESCE(MAX(id), 0) FROM placements").fetchone()[0]
    
    count = 0
    for idx, job in enumerate(jobs, start=current_max + 1):
        company = job.get("company", {}).get("display_name", "Unknown Company")
        role = job.get("title", "Tech Role")
        role = role.replace("<strong>", "").replace("</strong>", "")
        
        # Extract location hierarchy (city / area)
        location_area = job.get("location", {}).get("area", [])
        location = location_area[-1] if location_area else "UK Nationwide"
        
        # Calculate average salary or fallback benchmark
        salary_max = job.get("salary_max")
        salary_min = job.get("salary_min")
        if salary_max and salary_min:
            salary = int((salary_max + salary_min) / 2)
        elif salary_min:
            salary = int(salary_min)
        else:
            salary = 38000
            
        # Deduplication check
        exists = conn.execute(
            "SELECT COUNT(*) FROM placements WHERE company = ? AND role = ?", 
            [company, role]
        ).fetchone()[0]
        
        if exists == 0:
            conn.execute(
                "INSERT INTO placements VALUES (?, ?, ?, ?, ?)",
                [idx, company, role, location, salary]
            )
            count += 1
            
    conn.close()
    print(f"[SUCCESS] Pipeline Sync Complete. Added {count} new unique records to DuckDB!")

if __name__ == "__main__":
    sync_api_to_db()