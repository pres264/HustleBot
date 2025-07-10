import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def match_jobs(skills, top_n=3):
    """Match user skills against job database"""
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    
    # Get all jobs from database
    cursor.execute("SELECT id, title, description, required_skills FROM jobs")
    jobs = cursor.fetchall()
    
    if not jobs:
        return []
    
    # Prepare data for matching
    job_ids = [job[0] for job in jobs]
    job_texts = [f"{job[1]} {job[2]} {job[3]}" for job in jobs]
    
    # Vectorize and compare
    vectorizer = TfidfVectorizer()
    job_vectors = vectorizer.fit_transform(job_texts)
    user_vector = vectorizer.transform([" ".join(skills)])
    
    # Calculate similarity scores
    similarities = cosine_similarity(user_vector, job_vectors)
    top_indices = similarities.argsort()[0][-top_n:][::-1]
    
    # Prepare results
    matched_jobs = []
    for idx in top_indices:
        matched_jobs.append({
            'id': jobs[idx][0],
            'title': jobs[idx][1],
            'match_score': float(similarities[0][idx])
        })
    
    return matched_jobs