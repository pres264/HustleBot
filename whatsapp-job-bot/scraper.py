import requests
from bs4 import BeautifulSoup

def scrape_brightermonday_jobs(keywords):
    results = []
    base_url = "https://www.brightermonday.co.ke/jobs?q="
    headers = {"User-Agent": "Mozilla/5.0"}

    for keyword in keywords:
        url = base_url + keyword
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = soup.find_all("a", href=True)
            for job in job_cards:
                if job.find("h3"):
                    title = job.find("h3").text.strip()
                    link = "https://www.brightermonday.co.ke" + job["href"]
                    results.append({
                        "title": title,
                        "company": {"display_name": "BrighterMonday"},
                        "location": {"display_name": "Kenya"},
                        "url": link,
                    })
    return results

def scrape_opportunitiesforyoungkenyans():
    results = []
    url = "https://opportunitiesforyoungkenyans.co.ke/feed/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "xml")  # It's an RSS feed
        items = soup.find_all("item")
        for item in items[:10]:
            results.append({
                "title": item.title.text,
                "company": {"display_name": "OpportunitiesForYoungKenyans"},
                "location": {"display_name": "Kenya"},
                "url": item.link.text
            })
    except Exception as e:
        print("❌ Failed to fetch OpportunitiesForYoungKenyans:", str(e))
    return results

def scrape_greenhouse_jobs():
    results = []
    url = "https://boards.greenhouse.io/embed/job_board?for=zipline"  # Zipline example
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.select("a.posting-title")
        for job in jobs:
            title = job.text.strip()
            link = "https://boards.greenhouse.io" + job["href"]
            results.append({
                "title": title,
                "company": {"display_name": "Zipline (Greenhouse)"},
                "location": {"display_name": "Kenya"},  # Or extract location from parent tag
                "url": link
            })
    except Exception as e:
        print("❌ Failed to fetch Greenhouse jobs:", str(e))
    return results

def scrape_all_jobs(keywords):
    # Combine jobs from all platforms
    print("🔍 Scraping BrighterMonday...")
    bm_jobs = scrape_brightermonday_jobs(keywords)

    print("🔍 Scraping OpportunitiesForYoungKenyans...")
    ofyk_jobs = scrape_opportunitiesforyoungkenyans()

    print("🔍 Scraping Greenhouse...")
    gh_jobs = scrape_greenhouse_jobs()

    all_jobs = bm_jobs + ofyk_jobs + gh_jobs
    print(f"✅ Total jobs collected: {len(all_jobs)}")
    return all_jobs
