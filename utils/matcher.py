from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.preprocessor import clean_text, extract_keywords


def compute_match_score(resume_text: str, jd_text: str) -> float:
    """
    Compute cosine similarity between resume and job description
    using TF-IDF vectorization.
    Returns score as percentage (0-100).
    """
    cleaned_resume = clean_text(resume_text)
    cleaned_jd = clean_text(jd_text)

    if not cleaned_resume or not cleaned_jd:
        return 0.0

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([cleaned_resume, cleaned_jd])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(score * 100, 2)


def get_matched_keywords(resume_text: str, jd_text: str) -> dict:
    """
    Find which JD keywords are present and missing in the resume.
    Returns dict with 'matched' and 'missing' keyword lists.
    """
    resume_keywords = set(extract_keywords(resume_text, top_n=50))
    jd_keywords = set(extract_keywords(jd_text, top_n=50))

    matched = list(jd_keywords & resume_keywords)
    missing = list(jd_keywords - resume_keywords)

    return {
        "matched": sorted(matched),
        "missing": sorted(missing),
        "total_jd_keywords": len(jd_keywords),
        "match_count": len(matched)
    }


def get_score_feedback(score: float) -> dict:
    """
    Return label, color, and suggestion based on score.
    """
    if score >= 75:
        return {
            "label": "Excellent Match! 🎉",
            "color": "#22c55e",
            "suggestion": "Your resume aligns very well with this job. Apply with confidence!"
        }
    elif score >= 50:
        return {
            "label": "Good Match 👍",
            "color": "#f59e0b",
            "suggestion": "Solid match. Add a few missing keywords to strengthen your application."
        }
    elif score >= 30:
        return {
            "label": "Partial Match ⚠️",
            "color": "#f97316",
            "suggestion": "You meet some requirements. Tailor your resume to include more JD keywords."
        }
    else:
        return {
            "label": "Low Match ❌",
            "color": "#ef4444",
            "suggestion": "Your resume needs significant tailoring for this role. Focus on missing keywords."
        }