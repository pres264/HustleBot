from scraper import scrape_all_jobs

print("🚀 Starting job scrape test...")

try:
    # 🔎 Perform scraping once
    results = scrape_all_jobs(["IT"])

    print(f"✅ Total jobs found: {len(results)}")

    # Show the first 3 jobs for inspection
    for i, job in enumerate(results[:3]):
        print(f"\n🔹 Job {i+1}:")
        print(f"Title: {job.get('title')}")
        print(f"Company: {job.get('company')}")
        print(f"Location: {job.get('location')}")
        print(f"Link: {job.get('url')}")
    
except Exception as e:
    print("❌ Scraping failed:", e)
