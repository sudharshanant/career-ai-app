import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Example dataset (replace with real skills + career data)
texts = [
    "python machine learning AI NLP", 
    "network security ethical hacking cyber security", 
    "web development javascript html css",
    "data analysis python SQL business intelligence"
]
labels = [
    "Machine Learning Engineer",
    "Cyber Security Analyst",
    "Web Developer",
    "Data Analyst"
]

# Vectorize text
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)
y = labels

# Train model
model = LogisticRegression(max_iter=1000, multi_class='auto')
model.fit(X, y)

# Save model and vectorizer
with open("model/career_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("model/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
