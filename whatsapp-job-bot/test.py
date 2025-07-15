from scraper import scrape_all_jobs

print("🚀 Starting job scrape test...")

results = scrape_all_jobs(["IT"])

print(f"🔍 Total jobs found: {len(results)}")
for i, job in enumerate(results[:3]):
    print(f"\n🔹 Job {i+1}:")
    print(job)
    print("💡 Starting scrape_brightermonday_jobs...")
    print("📄 Page Content Preview:")
    print(response.text[:500])
try:
    results = scrape_all_jobs(["IT"])
    print(f"✅ Total jobs found: {len(results)}")
except Exception as e:
    print("❌ Scraping failed:", e)


