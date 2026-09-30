# UK Tech Placement Insights Dashboard

An end-to-end data engineering pipeline and interactive analytics dashboard designed to monitor and analyze software and data science placement trends across the UK.

---

## Key Features

- **Automated ETL Pipeline**: Multi-page ingestion from the Adzuna REST API with custom deduplication and schema transformation.
- **High-Performance Analytical Engine**: Utilizes DuckDB for optimized OLAP in-memory SQL queries.
- **Interactive UI & Search**: Real-time fuzzy keyword search and dynamic filtering built with Streamlit.
- **Resilient Architecture**: Built-in fallback mechanisms and parameterized SQL querying to prevent SQL injection.

---

## Architecture & Tech Stack

- **Frontend / UX**: Streamlit
- **Database / Analytics**: DuckDB
- **Data Source**: Adzuna Job Search API
- **Language & Libraries**: Python 3.x, Pandas, Requests, Python-Dotenv

---

## Getting Started

### 1. Prerequisites

Ensure you have Python 3.10+ installed.

### 2. Installation

Clone the repository and set up a virtual environment:

```bash
git clone https://github.com/zzh710/uk_tech_placement_insights.git
cd uk_tech_placement_insights
python -m venv .venv
source .venv/bin/activate  
pip install -r requirements.txt
```
### 3. Environment Setup

Create a `.env` file in the root directory and add your Adzuna API credentials:

```env
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```

### 4. Run Data Pipeline & Dashboard

Sync real-time data from the API into DuckDB:

```bash
python -m src.fetch_api
```

Launch the Streamlit dashboard:

```bash
streamlit run app.py
```

---


## Dashboard Preview

- **Total Openings & Metrics**: Real-time computation of average salary and high-density tech hubs.

- **Top 10 Salary Analytics**: Dynamic bar charts showcasing top-paying cities and hiring organizations.

- **Data Table**: Filterable view of current job opportunities with parameterized search.