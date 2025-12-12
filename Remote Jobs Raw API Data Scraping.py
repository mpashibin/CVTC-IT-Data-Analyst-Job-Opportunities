import requests
import pandas as pd
from datetime import datetime


# CONFIGURATION

ADZUNA_APP_ID = "7dc38b9b"                                  # Edit with your App ID
ADZUNA_APP_KEY = "fdda72b53bf62ea249ca09e519c183fe"         # Edit with your App Key
COUNTRY = "us"
RESULTS_PER_PAGE = 50
PAGES_TO_COLLECT = 3   
SEARCH_TERM = "data analyst remote"


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


# MAIN SCRAPING PROCESS

all_jobs = []

print("Collecting remote data analyst jobs...")

for page in range(1, PAGES_TO_COLLECT + 1):
    try:
        jobs = fetch_jobs(SEARCH_TERM, page)
        for job in jobs:
            all_jobs.append(job)
    except Exception as e:
        print(f"Error fetching data on page {page}: {e}")

print(f"Total jobs collected: {len(all_jobs)}")

# Convert list of dicts to DataFrame
df = pd.DataFrame(all_jobs)

# Add timestamp column
df["run_timestamp"] = datetime.now()

# SAVE TO FILE FOR DATA CLEANSING/TRANSFORMATION AND IMPORT

excel_filename = "remote_data_analyst_jobs.xlsx"
df.to_excel(excel_filename, index=False)

print(f"\nSaved all data to: {excel_filename}")
print("Done!")
