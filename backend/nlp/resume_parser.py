import spacy
import re

# Try to load the model, with fallback
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If model not found, download it
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

SKILLS_DB = [
    'python', 'java', 'sql', 'flask', 'django',
    'machine learning', 'data analysis', 'aws',
    'javascript', 'html', 'css', 'react'
]

def extract_skills(text):
    """Extract skills from text using NLP and pattern matching"""
    doc = nlp(text.lower())
    skills = set()
    
    # Extract nouns and noun phrases
    for chunk in doc.noun_chunks:
        if chunk.text in SKILLS_DB:
            skills.add(chunk.text)
    
    # Extract skills using pattern matching
    tokens = [token.text for token in doc if not token.is_stop]
    for token in tokens:
        if token in SKILLS_DB:
            skills.add(token)
    
    return list(skills)