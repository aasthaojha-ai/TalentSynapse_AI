from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Tuple, Any

def get_tfidf_vectors(resume_text: str, job_desc_text: str) -> Tuple[Any, Any]:
    """
    Converts the resume text and job description into TF-IDF vectors.
    Returns the sparse matrix of vectors and the fitted vectorizer object.
    """
    # Guard clause to handle empty inputs and prevent TfidfVectorizer ValueError
    if not resume_text.strip() or not job_desc_text.strip():
        return None, None
        
    vectorizer = TfidfVectorizer()
    documents = [resume_text, job_desc_text]
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    return tfidf_matrix, vectorizer

def calculate_similarity(tfidf_matrix: Any) -> float:
    """
    Calculates the cosine similarity between the resume (index 0) 
    and the job description (index 1).
    """
    if tfidf_matrix is None:
        return 0.0
        
    match_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    score = match_matrix[0][0]
    return float(score)
