from flask import Flask, request, jsonify
from utils.twilio_handler import process_whatsapp_message
from nlp.resume_parser import extract_skills
from nlp.matcher import match_jobs
import sqlite3
import os

app = Flask(__name__)

# Database configuration
DATABASE = 'jobs.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Twilio WhatsApp webhook
@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    user_msg = request.form.get('Body', '').strip()
    phone_number = request.form.get('From', '').split(':')[-1]
    
    # Process message through pipeline
    skills = extract_skills(user_msg)
    matched_jobs = match_jobs(skills)
    response = process_whatsapp_message(phone_number, matched_jobs)
    
    return str(response)

# API endpoint for job matching
@app.route('/api/match', methods=['POST'])
def api_match():
    data = request.json
    skills = extract_skills(data.get('text', ''))
    matched_jobs = match_jobs(skills)
    return jsonify({'jobs': matched_jobs})

if __name__ == '__main__':
    # Initialize database if not exists
    if not os.path.exists(DATABASE):
        with get_db() as conn:
            with open('schema.sql') as f:
                conn.executescript(f.read())
    app.run(debug=True)