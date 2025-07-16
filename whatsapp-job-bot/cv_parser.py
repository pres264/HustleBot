import fitz  # PyMuPDF
import docx
import os
import spacy
from collections import Counter
import re

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("⚠️ spaCy model not found. Run: python -m spacy download en_core_web_sm")
    raise

EXTRA_STOPWORDS = {
    "experience", "skills", "knowledge", "project", "projects", "responsible",
    "ability", "etc", "also", "using", "role", "including", "year", "years",
    "cv", "curriculum vitae"
}

def extract_text_from_cv(filepath):
    text = ""
    _, ext = os.path.splitext(filepath)

    if ext.lower() == '.pdf':
        try:
            doc = fitz.open(filepath)
            for page in doc:
                text += page.get_text()
            doc.close()
        except Exception as e:
            raise RuntimeError(f"Error reading PDF: {e}")

    elif ext.lower() == '.docx':
        try:
            doc = docx.Document(filepath)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            raise RuntimeError(f"Error reading DOCX: {e}")
    else:
        raise ValueError("Unsupported file type: only PDF and DOCX are supported.")

    if not text.strip():
        raise ValueError("The extracted CV text is empty.")

    return text

def extract_keywords(text, top_n=10):
    doc = nlp(text)

    noun_phrases = [chunk.text.lower().strip() for chunk in doc.noun_chunks]
    entities = [ent.text.lower().strip() for ent in doc.ents if ent.label_ in {
        "ORG", "PRODUCT", "SKILL", "WORK_OF_ART", "PERSON", "GPE", "NORP"
    }]
    tokens = [
        token.text.lower()
        for token in doc
        if token.pos_ in ("NOUN", "PROPN")
        and not token.is_stop
        and token.is_alpha
    ]

    all_terms = noun_phrases + entities + tokens
    cleaned = []
    for phrase in all_terms:
        phrase = re.sub(r'\s+', ' ', phrase.strip())
        if phrase not in EXTRA_STOPWORDS and len(phrase) > 1:
            cleaned.append(phrase)

    most_common = Counter(cleaned).most_common(top_n)
    return [word for word, _ in most_common]
