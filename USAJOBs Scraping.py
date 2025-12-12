import requests
import pandas as pd
from datetime import datetime

# CONFIGURATION

USER_AGENT = ""                                             # Enter your email used for API Key
API_KEY = "b6Pt023Euzm6F0POKgN/q9GdIvNDnf/5denhj2Wf0xQ="    # Enter your API Key

SEARCH_TERM = "analyst"
REMOTE_ONLY = True                                          # Change to false if you want all jobs
RESULTS_PER_PAGE = 50
PAGES_TO_FETCH = 5


# API REQUEST FUNCTION

def fetch_usajobs(page):
    url = "https://data.usajobs.gov/api/search"

    params = {
        "Keyword": SEARCH_TERM,
        "Page": page,
        "ResultsPerPage": RESULTS_PER_PAGE
    }

    # Filter for remote jobs
    if REMOTE_ONLY:
        params["LocationName"] = "Remote"

    headers = {
        "User-Agent": USER_AGENT,
        "Authorization-Key": API_KEY
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

# MAIN SCRAPING LOOP

all_jobs = []

print("Collecting USAJOBS listings...")

for page in range(1, PAGES_TO_FETCH + 1):
    try:
        data = fetch_usajobs(page)
        jobs = data.get("SearchResult", {}).get("SearchResultItems", [])

        for job in jobs:
            descriptor = job.get("MatchedObjectDescriptor", {})
            all_jobs.append(descriptor)

    except Exception as e:
        print(f"Error fetching page {page}: {e}")

print(f"Total jobs collected: {len(all_jobs)}")

# CONVERT TO DATAFRAME

df = pd.DataFrame(all_jobs)

# add timestamp
df["run_timestamp"] = datetime.now()


# SAVE TO EXCEL FILE FOR DATA CLEANSING/TRANSFORMATION

excel_filename = "usajobs_analyst.xlsx"
df.to_excel(excel_filename, index=False)

print(f"\nSaved USAJOBS data to: {excel_filename}")
print("Done!")
