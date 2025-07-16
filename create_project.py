import os
from pathlib import Path

# Project structure
structure = {
    ".vscode": {
        "settings.json": "{}",
        "launch.json": "{}"
    },
    "backend": {
        "nlp": {
            "matcher.py": "import spacy\nnlp = spacy.load('en_core_web_sm')\n\ndef match_jobs(user_skills, jobs):\n    # Implement matching logic\n    return []",
            "resume_parser.py": "def extract_skills(text):\n    # Implement skills extraction\n    return []"
        },
        "utils": {
            "scraper.py": "from bs4 import BeautifulSoup\nimport requests\n\ndef scrape_jobs():\n    # Implement scraping\n    return []",
            "bias_filter.py": "def anonymize_resume(text):\n    # Remove personal info\n    return text",
            "twilio_handler.py": "def process_message(msg):\n    # Process WhatsApp messages\n    return 'Reply message'"
        },
        "__init__.py": "",
        "app.py": """from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    user_msg = request.form.get('Body', '').strip()
    resp = MessagingResponse()
    resp.message(f"You said: {user_msg}")
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True)""",
        "models.py": """from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True)
    skills = db.Column(db.String(500))""",
        "config.py": "TWILIO_ACCOUNT_SID = ''\nTWILIO_AUTH_TOKEN = ''"
    },
    "tests": {
        "test_nlp.py": "def test_sample():\n    assert True",
        "test_twilio.py": "def test_sample():\n    assert True"
    },
    ".gitignore": "venv/\n.env\n*.pyc\n__pycache__/",
    "requirements.txt": """flask==2.0.1
flask-sqlalchemy==3.0
twilio==7.0.0
spacy==3.0
beautifulsoup4==4.9.3""",
    "README.md": "# WhatsApp Job Bot\nAI-powered job matching via WhatsApp"
}

def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        elif isinstance(content, list):
            os.makedirs(path, exist_ok=True)
            for item in content:
                Path(os.path.join(path, item)).touch()
        else:
            with open(path, "w") as f:
                f.write(content)

# Create project in current directory
create_structure(".", structure)

print("✅ Project structure created successfully!")