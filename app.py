import streamlit as st
import pandas as pd
from src.db import get_connection, init_db

# Page layout
st.set_page_config(
    page_title="UK Tech Placement Insights",
    page_icon="💼",
    layout="wide"
)

# Initialize
init_db()

# Intro
st.title("UK Tech Placement Insights Dashboard")
st.subheader("Explore the latest software & data placement statistics across the UK")

# Retrieve locations via SQL
conn = get_connection()
location_records = conn.execute("SELECT DISTINCT location FROM placements ORDER BY location").fetchall()
conn.close()

# List of locations from query
all_locations = [rec[0] for rec in location_records]

# Sidebar
st.sidebar.header("Filter & Search Options")

# Keyword search bar for role or company
search_term = st.sidebar.text_input("🔍 Search Keyword", placeholder="e.g. Data, Developer, Google")

# Dropdown menu for location filtering
locations = ["All"] + all_locations
selected_location = st.sidebar.selectbox("Select Location", locations)

# Construct dynamic SQL
conn = get_connection()
query = "SELECT * FROM placements WHERE 1=1"
params = []

# Apply location filter
if selected_location != "All":
    query += " AND location = ?"
    params.append(selected_location)

# Apply fuzzy search filter across role and company
if search_term.strip():
    query += " AND (role ILIKE ? OR company ILIKE ?)"
    keyword_pattern = f"%{search_term.strip()}%"
    params.extend([keyword_pattern, keyword_pattern])

# Execute optimized SQL query and load into DataFrame
df_filtered = conn.execute(query, params).df()
conn.close()

# Display summary metrics
st.markdown("### Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Openings", len(df_filtered))

if not df_filtered.empty:
    avg_salary = int(df_filtered["salary_gbp"].mean())
    top_location = df_filtered["location"].mode()[0] if not df_filtered["location"].empty else "N/A"
    col2.metric("Average Salary (GBP)", f"£{avg_salary:,}")
    col3.metric("Top Location", top_location)
else:
    col2.metric("Average Salary (GBP)", "N/A")
    col3.metric("Top Location", "N/A")

# Visualizations Section
st.markdown("### Analytics & Insights")
if not df_filtered.empty:
    chart_col1, chart_col2 = st.columns(2)
    
    # Chart 1: Top 10 Average Salary by Location
    with chart_col1:
        st.markdown("#### Top 10 Average Salary by City")
        avg_salary_by_loc = (
            df_filtered.groupby("location")["salary_gbp"]
            .mean()
            .reset_index()
            .sort_values(by="salary_gbp", ascending=False)
            .head(10)
        )
        st.bar_chart(avg_salary_by_loc.set_index("location")["salary_gbp"], horizontal=True, color="#1f77b4")
        
    # Chart 2: Top 10 Companies by Jobs
    with chart_col2:
        st.markdown("#### Top 10 Companies by Openings")
        company_counts = (
            df_filtered["company"]
            .value_counts()
            .reset_index()
        )
        company_counts.columns = ["company", "count"]
        company_counts = company_counts.head(10)
        st.bar_chart(company_counts.set_index("company")["count"], horizontal=True, color="#ff7f0e")
else:
    st.info("No placement data found matching your search and filter criteria.")

# Display
st.markdown("### Placement Listings")
st.dataframe(df_filtered, width="stretch")