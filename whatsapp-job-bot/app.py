from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
from werkzeug.utils import secure_filename
from cv_parser import extract_text_from_cv
from job_api import search_jobs
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# 🔍 Log every incoming request method and path
@app.before_request
def log_request():
    print(f"👉 {request.method} {request.path}")

# ✅ Simple homepage to confirm Flask is running
@app.route('/', methods=['GET'])
def home():
    return "✅ WhatsApp job bot is running!"

# 📩 WhatsApp webhook
@app.route('/webhook', methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').lower()
    
    media_url = request.values.get('MediaUrl0', None)
    media_type = request.values.get('MediaContentType0', None)

    print(f"Incoming message: {incoming_msg}")
    print(f"Media: {media_url}({media_type})")

    resp = MessagingResponse()
    msg = resp.message()

    if 'hello' in incoming_msg:
        msg.body("👋 Hi! Please upload your CV (PDF or DOCX) to get tailored job matches.")
    elif media_url and media_type in ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        # Get the file from Twilio's Media URL
        twilio_auth = (os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        response = requests.get(media_url, auth=twilio_auth)

        if response.status_code == 200:
            filename = secure_filename(f"user_cv.{media_type.split('/')[-1]}")
            filepath = os.path.join("cv_uploads", filename)
            os.makedirs("cv_uploads", exist_ok=True)

            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"✅ CV saved to {filepath}")
            msg.body("📄 CV received! Analyzing now...")

            #extract text and key words from the cv
            text = extract_text_from_cv(filepath)
            print("🧠 Extracted CV Text Preview:")
            print(text[:1000]) # Preview first 1000 characters
            keywords = extract_keywords(text, top_n=7)
            print

            msg.body("📝 CV analysis complete! We will match you with suitable job opportunities shortly based on your qualifications."  )

            # 🔎 Search for matching jobs using Adzuna
            job_results = search_jobs(keywords, location="kenya")

            # 💬 Format the response
            if job_results:
                reply = "📌 Here are some jobs matching your CV:\n\n"
                for job in job_results:
                    title = job.get("title", "No title")
                    company = job.get("company", {}).get("display_name", "Unknown")
                    location = job.get("location", {}).get("display_name", "Unknown")
                    url = job.get("redirect_url", "#")

                    reply += f"🔹 *{title}*\nCompany: {company}\nLocation: {location}\nLink: {url}\n\n"
            else:
                reply = "😕 Couldn't find any job matches right now. Try again later."

            msg.body(reply)
            print("📬 Sending job matches to user...")

            # Optionally, you can delete the file after processing
            #os.remove(filepath)
        else:
            msg.body("❌ Failed to download your CV. Please try again.")

    else:
        msg.body("Send 'hello' to get started or upload your CV directly.")
    
    return str(resp)

# 🚀 Start the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

