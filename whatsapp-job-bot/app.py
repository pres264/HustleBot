from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
from werkzeug.utils import secure_filename
from cv_parser import extract_text_from_cv, extract_keywords
from scraper import scrape_all_jobs
from cv_model import CVUpload, session
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.before_request
def log_request():
    print(f"👉 {request.method} {request.path}")

@app.route('/', methods=['GET'])
def home():
    return "✅ WhatsApp job bot is running!"

@app.route('/webhook', methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').lower()
    media_url = request.values.get('MediaUrl0', None)
    media_type = request.values.get('MediaContentType0', None)

    print(f"Incoming message: {incoming_msg}")
    print(f"Media: {media_url} ({media_type})")

    resp = MessagingResponse()
    msg = resp.message()

    if 'hello' in incoming_msg:
        msg.body("👋 Hi! Please upload your CV (PDF)to get tailored job matches.")

    elif media_url and media_type in ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        twilio_auth = (os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        response = requests.get(media_url, auth=twilio_auth)

        if response.status_code == 200:
            ext = media_type.split('/')[-1]
            base_name = "user_cv"
            counter = 0
            os.makedirs("cv_uploads", exist_ok=True)

            while True:
                filename = f"{base_name}_{counter}.{ext}" if counter else f"{base_name}.{ext}"
                filepath = os.path.join("cv_uploads", secure_filename(filename))
                if not os.path.exists(filepath):
                    break
                counter += 1

            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"✅ CV saved to {filepath}")
            job_text = "📄 CV received! Hold on while we match you with jobs...\n"
            job_text += "🔍 Analyzing your CV and finding job matches...\n\n"

            # Save metadata
            cv_record = CVUpload(filename=filename, filepath=filepath)
            session.add(cv_record)
            session.commit()

            try:
                text = extract_text_from_cv(filepath)
                print("🧠 Extracted CV Text Preview:")
                print(text[:500])  # Preview only

                keywords = extract_keywords(text, top_n=7)
                print("🔑 Extracted Keywords:", keywords)

                # Scrape jobs
                print("🔍 Scraping jobs...")
                job_results = scrape_all_jobs(keywords)
                print("📊 Scraped Job Results:", job_results)

                if job_results:
                    job_text += "📌 Here are some jobs matching your CV:\n\n"
                    for job in job_results[:10]:
                        title = job.get("title", "No title")
                        company = job.get("company", {}).get("display_name", "Unknown")
                        location = job.get("location", {}).get("display_name", "Unknown")
                        url = job.get("url") or job.get("redirect_url") or "#"
                        job_text += f"🔹 *{title}*\n📍 {company}, {location}\n🔗 {url}\n\n"
                

                        if isinstance(company, dict):
                            company = company.get("display_name", "Unknown")
                        if isinstance(location, dict):
                            location = location.get("display_name", "Unknown")

                        job_text += f"🔹 *{title}*\n📍 {company}, {location}\n🔗 {url}\n\n"

                   
                else:
                    msg.body("😕 Sorry, no job matches found right now. Try again later!")

                msg.body(job_text)
                return str(resp)

            except Exception as e:
                print("❌ Error during analysis or scraping:", str(e))
                msg.body("⚠️ Error analyzing your CV. Please try again later.")

        else:
            msg.body("❌ Failed to download your CV. Please try again.")

    else:
        msg.body("Send 'hello' to get started or upload your CV directly.")

    return str(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
