import re
from sklearn.feature_extraction.text import CountVectorizer

def extract_keywords_from_text(text: str, max_keywords: int = 20) -> list:
    """
    Extract important keywords from the job description using basic NLP.
    """
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    words = text.lower().split()
    
    # Common boring words we ignore
    stopwords = set([
        "and", "or", "the", "with", "a", "an", "to", "of", "for", "in", "on",
        "at", "by", "from", "as", "is", "are", "will", "be", "you", "we", "your",
        "this", "that", "it", "skills", "experience", "knowledge", "using", "proficient",
        "understanding"
    ])
    
    # Count word frequencies
    vectorizer = CountVectorizer(stop_words="english")
    word_counts = vectorizer.fit_transform([text])
    word_freq = dict(zip(vectorizer.get_feature_names_out(), word_counts.toarray()[0]))
    
    # Filter out short/meaningless words
    filtered = {word: freq for word, freq in word_freq.items() if word not in stopwords and len(word) > 2}
    
    # Sort by frequency and get top N
    sorted_keywords = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    top_keywords = [word for word, freq in sorted_keywords[:max_keywords]]
    
    return top_keywords

def calculate_fit_score(resume_text: str, job_description: str) -> float:
    """
    Dynamically calculate resume fit score based on extracted job description keywords.
    """
    # Step 1: Extract important keywords from job description
    jd_keywords = extract_keywords_from_text(job_description)
    
    # Step 2: Lowercase resume for matching
    resume_text_lower = resume_text.lower()
    
    # Step 3: Check how many JD keywords exist in resume
    matched_keywords = [keyword for keyword in jd_keywords if keyword in resume_text_lower]
    
    # Step 4: Score = (# of matched keywords) / (total keywords) * 100
    if not jd_keywords:
        return 0.0
    score = (len(matched_keywords) / len(jd_keywords)) * 100
    
    return round(score, 2)
