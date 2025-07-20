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
```
## 📲 How to Access the WhatsApp Job Bot

To interact with the WhatsApp Job Bot, follow these simple steps:

1. **Save the Twilio Sandbox Number**  
   Save this number in your contacts:  
   📞 `+14155238886` (Twilio Sandbox for WhatsApp)

2. **Join the Sandbox**  
   Open WhatsApp and send the following message to the saved number:
   ```
   join fighting-independent
   ```
   *This connects you to the sandbox environment where the bot lives.*

3. **Start the Bot**  
   Once you're successfully connected, send:
   ```
   hello
   ```
   The bot will reply with instructions on how to upload your CV.

4. **Upload Your CV**  
   Send your CV as a **PDF** or **DOCX** file.  
   The bot will analyze your resume and return a list of job opportunities tailored to your skills.
