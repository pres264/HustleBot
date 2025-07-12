import requests
import os

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")

def search_jobs(skills, location="kenya", max_results=5):
    query = " ".join(skills)

    url = f"https://api.adzuna.com/v1/api/jobs/ke/search/1"

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": max_results,
        "what": query,
        "where": location,
        "content-type": "application/json"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        jobs = response.json().get("results", [])
        return jobs
    else:
        print("❌ Adzuna API error:", response.status_code)
        return []
