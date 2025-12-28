from pdfminer.high_level import extract_text
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')

def extract_resume_text(pdf_path):
    text = extract_text(pdf_path)
    tokens = nltk.word_tokenize(text.lower())
    words = [w for w in tokens if w.isalpha() and w not in stopwords.words('english')]
    return " ".join(words)

def resume_match(resume_text, job_desc):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_desc])
    score = cosine_similarity(vectors[0:1], vectors[1:2])
    return round(score[0][0]*100, 2)
