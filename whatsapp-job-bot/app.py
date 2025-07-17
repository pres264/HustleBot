from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from requests.auth import HTTPBasicAuth
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
        msg.body("👋 Hi! Please upload your CV (PDF or DOCX) to get tailored job matches.")
        return str(resp)

    if media_url and media_type in [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]:
        # Securely authenticate with Twilio
        twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        twilio_token = os.getenv("TWILIO_AUTH_TOKEN")

        print(f"📡 Downloading from: {media_url}")
        response = requests.get(media_url, auth=HTTPBasicAuth(twilio_sid, twilio_token))

        print(f"📥 Status Code: {response.status_code}")
        if response.status_code == 200:
            ext = media_type.split('/')[-1]
            os.makedirs("cv_uploads", exist_ok=True)
            filename = secure_filename(f"user_cv.{ext}")
            filepath = os.path.join("cv_uploads", filename)

            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"✅ CV saved to {filepath}")
            msg.body("📄 CV received! Analyzing now...")

            # Save metadata to DB
            cv_record = CVUpload(filename=filename, filepath=filepath)
            session.add(cv_record)
            session.commit()

            try:
                text = extract_text_from_cv(filepath)
                print("🧠 Extracted CV text preview:", text[:500])
                keywords = extract_keywords(text, top_n=7)
                print("🔑 Extracted Keywords:", keywords)

                job_results = scrape_all_jobs(keywords)
                print(f"📊 Scraped Job Results: {len(job_results)}")

                if job_results:
                    job_list = "📌 Here are some jobs matching your CV:\n\n"
                    for job in job_results[:5]:
                        title = job.get("title", "No title")
                        company = job.get("company", {}).get("display_name", "Unknown")
                        location = job.get("location", {}).get("display_name", "Unknown")
                        url = job.get("url", "#")
                        job_list += f"🔹 *{title}*\n📍 {company}, {location}\n🔗 {url}\n\n"
                    msg.body(job_list)
                else:
                    msg.body("😕 No job matches found right now. Try again later.")

            except Exception as e:
                print("❌ Error during analysis or scraping:", str(e))
                msg.body("⚠️ There was an error analyzing your CV. Please try again later.")

            return str(resp)

        else:
            print(f"❌ Download failed: {response.status_code} — {response.text}")
            msg.body("❌ Failed to download your CV. Please try again.")
            return str(resp)

    msg.body("Send 'hello' to get started or upload your CV.")
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
