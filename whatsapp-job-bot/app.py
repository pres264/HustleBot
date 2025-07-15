from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
from werkzeug.utils import secure_filename
from cv_parser import extract_text_from_cv, extract_keywords
from scraper import scrape_all_jobs
from cv_model import cvUploads, session
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
    
    elif media_url and media_type in [
        'application/pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ]:
        twilio_auth = (os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        response = requests.get(media_url, auth=twilio_auth)

        if response.status_code == 200:
            filename = secure_filename(f"user_cv.{media_type.split('/')[-1]}")
            filepath = os.path.join("cv_uploads", filename)
            os.makedirs("cv_uploads", exist_ok=True)

            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"✅ CV saved to {filepath}")
            msg.body("📄 CV received! Hold on while we match you with jobs...")

            # Save meta data to database
            cv_record = CVUpload(filename=filename, filepath=filepath)
            session.add(cv_record)
            session.commit()
            print("💾 CV metadata saved to database.")
            
            try:
                text = extract_text_from_cv(filepath)
                print("🧠 Extracted CV Text Preview:")
                print(text[:1000])

                keywords = extract_keywords(text, top_n=7)
                print("🔑 Extracted Keywords:", keywords)

                # Let user know analysis is starting
                followup = MessagingResponse()
                followup.message("🔍 Analyzing your CV and finding job matches...")

                # Perform job scraping
                job_results = scrape_all_jobs(keywords)
                print("🔍 Scraped Job Results:", job_results)

                # Format and send jobs to user
                if job_results:
                    job_list = "📌 Here are some jobs matching your CV:\n\n"
                    for job in job_results[:3]:  # Send top 3
                        title = job.get("title", "No title")

                        # Fix company and location display names
                        company = job.get("company", "Unknown")
                        if isinstance(company, dict):
                            company = company.get("display_name", "Unknown")

                        location = job.get("location", "Unknown")
                        if isinstance(location, dict):
                            location = location.get("display_name", "Unknown")

                        # Get URL (ensure it's present)
                        url = job.get("url") or job.get("redirect_url") or "#"


                        job_list += f"🔹 *{title}*\n📍 {company}, {location}\n🔗 {url}\n\n"
                    
                    followup.message("📌 Here are some jobs matching your CV:\n\n" + job_list)
                else:
                    followup.message("😕 Sorry, we couldn't find any job matches for now. Try again later!")

                return str(followup)

            except Exception as e:
                print("❌ Error analyzing CV:", str(e))
                msg.body("⚠️ Sorry, there was an error processing your CV.")
        else:
            msg.body("❌ Failed to download your CV. Please try again.")
    
    else:
        msg.body("Send 'hello' to get started or upload your CV directly.")

    return str(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
