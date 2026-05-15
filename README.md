# 📄 Resume Screener — NLP-Powered Job Match Analyzer

> Upload your resume, paste a job description, and instantly see how well you match — with keyword gap analysis.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red?style=flat-square&logo=streamlit)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.4-orange?style=flat-square&logo=scikit-learn)
![NLTK](https://img.shields.io/badge/NLTK-3.8-green?style=flat-square)

---

## 🎯 What It Does

Most job seekers apply to roles without knowing how well their resume actually matches. This tool solves that by:

- **Extracting text** from your PDF resume automatically
- **Preprocessing** both resume and JD using NLP (tokenization, stopword removal, lemmatization)
- **Scoring the match** using TF-IDF vectorization + Cosine Similarity
- **Highlighting missing keywords** so you know exactly what to add
- **Giving actionable feedback** based on your score

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| PDF Extraction | PyPDF2 |
| NLP Preprocessing | NLTK |
| Vectorization | Scikit-learn (TF-IDF) |
| Similarity | Cosine Similarity |
| Visualization | Plotly |
| Frontend | Streamlit |
| Deployment | Streamlit Cloud |

---

## 📁 Project Structure

```
resume-screener/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Dependencies
├── README.md
│
└── utils/
    ├── extractor.py        # PDF text extraction
    ├── preprocessor.py     # NLP cleaning pipeline
    └── matcher.py          # TF-IDF scoring + keyword analysis
```

---

## 🚀 Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/resume-screener.git
cd resume-screener
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the app
```bash
streamlit run app.py
```

App opens at `http://localhost:8501`

---

## ☁️ Deploy on Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file as `app.py`
5. Click Deploy — live in ~2 minutes ✅

---

## 📊 How the Scoring Works

```
Resume Text ──► Clean & Tokenize ──► TF-IDF Vector ──┐
                                                       ├──► Cosine Similarity ──► Score %
Job Description ► Clean & Tokenize ──► TF-IDF Vector ──┘
```

| Score | Result |
|---|---|
| 75%+ | Excellent Match 🎉 |
| 50–74% | Good Match 👍 |
| 30–49% | Partial Match ⚠️ |
| Below 30% | Low Match ❌ |

---

## 💡 Key Features

- ✅ Upload PDF or paste resume text directly
- ✅ Keyword match & gap analysis
- ✅ Visual score gauge with color feedback
- ✅ Actionable improvement suggestions
- ✅ Clean dark UI with instant results

---

## 🔮 Future Improvements

- [ ] Sentence-BERT for semantic (not just keyword) matching
- [ ] Support DOCX resume uploads
- [ ] Bulk resume screening for recruiters
- [ ] Export report as PDF

---

## 👤 Author

**Aditya Rothe**
BSc Data Science Graduate
[LinkedIn](https://linkedin.com/in/aditya-rothe) • [GitHub](https://github.com/aditya-rothe)

---
[live app link](https://resume-screener-app-uftdqw3agfhxhqbov5nvfj.streamlit.app/)

*Built as part of my Data Science portfolio — showcasing end-to-end NLP project development and deployment.*
