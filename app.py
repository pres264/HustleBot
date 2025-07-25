from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from requests.auth import HTTPBasicAuth
import os
import requests
import urllib.parse
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

@app.route('/webhook', methods=['GET'])
def webhook_status():
    return "✅ Webhook is live and reachable! POST here with Twilio messages.", 200

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
        # --- Twilio secure media download ---
        twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
        client = Client(twilio_sid, twilio_token)
        print("TWILIO_ACCOUNT_SID:", twilio_sid)
        print("TWILIO_AUTH_TOKEN:", "✅ Loaded" if twilio_token else "❌ Missing")

        try:
            if "api.twilio.com" in media_url:
                # Split the path correctly
                path_parts = urllib.parse.urlsplit(media_url).path.strip("/").split("/")

                # Example URL: /2010-04-01/Accounts/{SID}/Messages/{MESSAGE_SID}/Media/{MEDIA_SID}
                message_sid_index = path_parts.index("Messages") + 1
                media_sid_index = path_parts.index("Media") + 1

                message_sid = path_parts[message_sid_index]
                media_sid = path_parts[media_sid_index]

                print("✅ Extracted Message SID:", message_sid)
                print("✅ Extracted Media SID:", media_sid)

                # Fetch media metadata using Twilio SDK
                media = client.messages(message_sid).media(media_sid).fetch()

                # Build the authenticated URL from media.uri (not media.url)
                media_url_authenticated = f"https://api.twilio.com{media.uri.replace('.json','')}"

                # Download the media
                response = requests.get(media_url_authenticated, auth=(twilio_sid, twilio_token))
                response.raise_for_status()
                media_bytes = response.content

            else:
                # Fallback for public URLs
                response = requests.get(media_url)
                response.raise_for_status()
                media_bytes = response.content

        except Exception as err:
            print("❌ Twilio media fetch failed:", err)
            msg.body("❌ Could not download your CV from WhatsApp. Please try again.")
            return str(resp)

        ext = media_type.split('/')[-1]
        os.makedirs("cv_uploads", exist_ok=True)
        filename = secure_filename(f"user_cv.{ext}")
        filepath = os.path.join("cv_uploads", filename)

        with open(filepath, "wb") as f:
            f.write(media_bytes)

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

    msg.body("Send 'hello' to get started or upload your CV.")
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
