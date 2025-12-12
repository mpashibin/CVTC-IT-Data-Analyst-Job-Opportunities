import requests
import pandas as pd
from datetime import datetime

# CONFIGURATION

ADZUNA_APP_ID = "7dc38b9b"                              # Edit with your App ID
ADZUNA_APP_KEY = "fdda72b53bf62ea249ca09e519c183fe"     # Edit with your App Key
COUNTRY = "us"
RESULTS_PER_PAGE = 50
PAGES_TO_COLLECT = 3
SEARCH_TERMS = [
    "data analyst",
    "business intelligence",
    "data science",
    "python",
    "SQL",
    "Power BI"
]

# API CALL FUNCTION

def fetch_jobs(query, page):
    url = f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/{page}"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": RESULTS_PER_PAGE,
        "what": query,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    return data.get("results", [])

# CLEANING FUNCTION

def parse_job(item):
    return {
        "job_title": item.get("title"),
        "company": item.get("company", {}).get("display_name"),
        "location": item.get("location", {}).get("display_name"),
        "category": item.get("category", {}).get("label"),
        "created_at": item.get("created"),
        "description": item.get("description"),
        "redirect_url": item.get("redirect_url"),
        "salary_min": item.get("salary_min"),
        "salary_max": item.get("salary_max"),
        "salary_avg": (
            (item.get("salary_min") or 0) + (item.get("salary_max") or 0)
        ) / 2,
    }


# MAIN SCRAPING PROCESS

all_jobs = []

print("Collecting jobs...")

for term in SEARCH_TERMS:
    for page in range(1, PAGES_TO_COLLECT + 1):
        try:
            jobs = fetch_jobs(term, page)
            for job in jobs:
                parsed = parse_job(job)
                parsed["search_query_used"] = term
                all_jobs.append(parsed)
        except Exception as e:
            print(f"Error fetching data for '{term}' on page {page}: {e}")

print(f"Total jobs collected: {len(all_jobs)}")

# Convert to DataFrame
df = pd.DataFrame(all_jobs)

# Add timestamp column
df["run_timestamp"] = datetime.now()


# SAVE TO FILES FOR TRANSFORMATION AND IMPORT

excel_filename = "job_listings.xlsx"

df.to_excel(excel_filename, index=False)

print(f"\nSaved data to:")
print(f" - {excel_filename}")
print("\nDone!")
