import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Ensure necessary NLTK data is available (already downloaded in step 1, but good practice)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')

def clean_text(text):
    """
    Cleans the input text by performing lowercase conversion, punctuation removal,
    tokenization, and stopword removal.
    """
    if not text:
        return ""
        
    # 1. Lowercase conversion
    text = text.lower()
    
    # 2. Punctuation removal
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # 3. Tokenization
    tokens = word_tokenize(text)
    
    # 4. Stopword removal
    stop_words = set(stopwords.words('english'))
    cleaned_tokens = [word for word in tokens if word not in stop_words and word.strip()]
    
    # Return as a structured space-separated string
    return " ".join(cleaned_tokens)

# Predefined skill database
SKILL_DATABASE = [
    "python", "sql", "machine learning", "power bi", "java", "c++", "c#", "data analysis", 
    "nlp", "deep learning", "tensorflow", "pytorch", "aws", "azure", "gcp", "docker", 
    "kubernetes", "git", "linux", "javascript", "react", "node.js", "html", "css",
    "excel", "tableau", "statistics", "mathematics", "agile", "scrum",
    "pandas", "numpy", "scikit-learn", "matplotlib", "seaborn", "keras", "opencv",
    "apache spark", "hadoop", "mongodb", "postgresql", "mysql", "snowflake",
    "langchain", "prompt engineering", "r", "generative ai"
]

def extract_skills(text):
    """
    Extracts skills from text by matching against a predefined skill database using regex.
    """
    text = text.lower()
    detected_skills = []
    
    for skill in SKILL_DATABASE:
        # Escape the skill to handle special characters like +, #, .
        escaped_skill = re.escape(skill)
        # Use lookarounds to ensure we match whole words only 
        # (prevents matching 'java' inside 'javascript')
        pattern = r'(?<!\w)' + escaped_skill + r'(?!\w)'
        
        if re.search(pattern, text):
            detected_skills.append(skill)
            
    return detected_skills
