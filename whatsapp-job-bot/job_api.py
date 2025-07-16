import requests
import os
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def search_jobs(skills, location="remote", max_results=5):
    if not RAPIDAPI_KEY:
        raise EnvironmentError("RAPIDAPI_KEY is missing in environment variables.")

    url = "https://job-search-api2.p.rapidapi.com/active-ats-expired"
    query = " ".join(skills)

    params = {
        "query": query,
        "num_pages": 1,
        "page": 1,
        "remote_jobs_only": "true",  # Could also try True without quotes
        "location": location
    }

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host":  "job-search-api2.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        jobs = response.json().get("data", [])
        return jobs[:max_results]
    else:
        print("❌ Failed to fetch jobs:", response.status_code, response.text)
        return []
