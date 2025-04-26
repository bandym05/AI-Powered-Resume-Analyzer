# backend/services/scorer.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_fit_score(resume_text: str, job_description: str) -> float:
    documents = [resume_text, job_description]
    tfidf = TfidfVectorizer().fit_transform(documents)
    score = cosine_similarity(tfidf[0:1], tfidf[1:2])
    return round(float(score[0][0]) * 100, 2)
