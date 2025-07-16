# HustleBot 🤖💼

An AI-powered WhatsApp chatbot that matches job seekers with relevant opportunities in Kenya and Africa.

(https://youtube.com/shorts/sPpWFZqupbw?si=O6l1leBCM-QNK0X1)  video demo use case

HustleBot is deeply committed to driving positive social change, aligning with several UN Sustainable Development Goals:

SDG 8: Decent Work and Economic Growth: Promoting full and productive employment and decent work for all, reducing unemployment rates by connecting people to jobs.

SDG 4: Quality Education: Incorporating potential for skills training and upskilling modules to enhance employability and lifelong learning opportunities.

SDG 10: Reduced Inequalities: Specifically targeting marginalised groups, such as women and rural youth, to ensure equitable access to economic opportunities and reduce disparities.

## Features ✨

- **CV Analysis**: Extracts skills from uploaded CVs
- **Smart Matching**: Recommends jobs based on skills
- **Bias-Free**: Anonymizes applications to reduce hiring bias
- **WhatsApp Integration**: Works entirely through WhatsApp
- **Localized**: Focused on African job markets

## Tech Stack 🛠️

- **Backend**: Python + Flask
- **NLP**: spaCy (skill extraction)
- **Database**: SQLite (PostgreSQL in production)
- **WhatsApp API**: Twilio
- **Hosting**: Render

## Setup Guide 🚀

### Prerequisites
- Python 3.8+
- Twilio account
- WhatsApp Business API access

### Installation
```bash
# Clone repository
git clone https://github.com/pres264/HustleBot.git
cd HustleBot/whatsapp-job-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export TWILIO_ACCOUNT_SID='your_sid'
export TWILIO_AUTH_TOKEN='your_token'
