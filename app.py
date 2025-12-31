from flask import Flask, render_template, request, redirect, session, url_for
from flask import Flask, render_template, request, redirect
import os
from resume_parser import extract_resume_text, resume_match

app = Flask(__name__)
app.secret_key = "career_ai_secret_key"

# Upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Career list with keywords
CAREERS = {
    "Software Engineer": ["python", "java", "c++", "programming", "software", "oop"],
    "Data Scientist": ["data", "statistics", "machine learning", "python", "analytics"],
    "Cyber Security Analyst": ["security", "cyber", "network", "firewall", "threat"],
    "AI Engineer": ["ai", "artificial intelligence", "deep learning", "nlp"],
    "Web Developer": ["html", "css", "javascript", "frontend", "backend"],
    "DevOps Engineer": ["devops", "docker", "kubernetes", "ci cd", "aws"],
    "Cloud Engineer": ["cloud", "aws", "azure", "gcp"],
    "Machine Learning Engineer": ["machine learning", "model", "training", "python"],
    "Data Analyst": ["sql", "excel", "dashboard", "data"],
    "Business Analyst": ["business", "requirements", "analysis"],
    "QA Engineer": ["testing", "automation", "selenium"],
    "UI/UX Designer": ["design", "figma", "ui", "ux"],
    "Mobile App Developer": ["android", "ios", "flutter", "react native"],
    "Game Developer": ["unity", "game", "c#", "graphics"],
    "Blockchain Developer": ["blockchain", "ethereum", "smart contract"],
    "IoT Engineer": ["iot", "sensors", "embedded"],
    "Network Engineer": ["network", "routing", "switching"],
    "System Administrator": ["linux", "server", "system"],
    "Database Administrator": ["sql", "database", "oracle"],
    "Product Manager": ["product", "roadmap", "stakeholder"]
}

@app.route('/recommend', methods=['POST'])
def recommend():
    skills = request.form.get('skills', '').lower()
    interest = request.form.get('interest', '').lower()
    hobbies = request.form.get('hobbies', '').lower()

    user_text = (skills + " " + interest + " " + hobbies)
    user_text = user_text.replace(',', ' ').replace('/', ' ')
    user_tokens = set(user_text.split())

    raw_scores = []

    for career, keywords in CAREERS.items():
        score = 0
        for kw in keywords:
            for token in kw.split():
                if token in user_tokens:
                    score += 1
        raw_scores.append((career, score))

    total_score = sum(score for _, score in raw_scores)

    results = []
    if total_score == 0:
        results = [(career, 0.0) for career, _ in raw_scores]
    else:
        for career, score in raw_scores:
            percent = round((score / total_score) * 100, 2)
            results.append((career, percent))

    results.sort(key=lambda x: x[1], reverse=True)
    results = results[:10]

    return render_template(
        'dashboard.html',
        results=results,
        skills=skills,
        interest=interest,
        hobbies=hobbies
    )
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Simple demo credentials
        if username == "admin" and password == "admin123":
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return render_template('signin.html', error="Invalid credentials")

    return render_template('signin.html')

@app.route('/resume')
def resume_upload():
    return render_template('resume_upload.html')

@app.route('/match', methods=['POST'])
def match():
    file = request.files.get('resume')
    job_desc = request.form.get('job_description', '')

    if not file:
        return "No file uploaded", 400

    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)

    resume_text = extract_resume_text(path)
    score = resume_match(resume_text, job_desc)

    return render_template('dashboard.html', score=score)

@app.route('/')
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/recommend-back')
def recommend_back():
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

