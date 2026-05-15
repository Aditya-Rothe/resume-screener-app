import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
def download_nltk_data():
    packages = ['stopwords', 'punkt', 'wordnet', 'omw-1.4', 'punkt_tab']
    for pkg in packages:
        try:
            nltk.download(pkg, quiet=True)
        except:
            pass

download_nltk_data()

lemmatizer = WordNetLemmatizer()
STOP_WORDS = set(stopwords.words('english'))


def clean_text(text: str) -> str:
    """
    Full NLP preprocessing pipeline:
    1. Lowercase
    2. Remove special characters & numbers
    3. Tokenize
    4. Remove stopwords
    5. Lemmatize
    """
    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Remove email addresses
    text = re.sub(r'\S+@\S+', '', text)

    # Remove special characters, digits, punctuation
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords and short tokens, then lemmatize
    tokens = [
        lemmatizer.lemmatize(token)
        for token in tokens
        if token not in STOP_WORDS and len(token) > 2
    ]

    return ' '.join(tokens)


def extract_keywords(text: str, top_n: int = 30) -> list:
    """
    Extract top keywords from text by frequency after preprocessing.
    """
    cleaned = clean_text(text)
    tokens = cleaned.split()
    freq = {}
    for token in tokens:
        freq[token] = freq.get(token, 0) + 1
    sorted_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_keywords[:top_n]]