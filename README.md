🤖 AI Resume Screening System

An intelligent AI-powered Resume Screening and Candidate Analysis platform built using Streamlit, NLP, and Machine Learning.

This system automatically ranks resumes against a job description, detects matched and missing technical skills, generates AI-based summaries, and provides recruiter-friendly analytics — all in a clean interactive dashboard.

🚀 Live Demo

🔗 Add your Streamlit Cloud deployment link here after deployment

📌 Overview

Recruiters often spend hours manually reviewing resumes.
This project automates the first screening round using:

Semantic similarity matching

Skill extraction using NLP

Named Entity Recognition (NER)

Technical skill coverage analysis

AI-generated candidate summaries

It significantly reduces manual effort and improves candidate shortlisting accuracy.

✨ Key Features
🔍 1. Resume Ranking (Semantic Matching)

Uses NLP-based similarity scoring

Compares resume content with job description

Displays match percentage

Automatically identifies Top Candidate

🧠 2. Advanced Skill Detection

Skill detection works in two ways:

✔ Predefined Master Skills (skills.json)

Large technical skill database

Covers AI, ML, Web, Cloud, DevOps, Data, etc.

✔ Dynamic Skill Extraction (spaCy NER)

Detects unknown tech terms

Extracts product & organization entities

Prevents skill misses

📊 3. Skill Match Analysis

For each candidate:

✅ Matched Skills

❌ Missing Skills

📈 Skill Coverage Percentage

Progress bar visualization

🧠 4. AI Resume Summary

Automatically generates:

📌 Candidate Level (Entry / Mid / Senior)

💼 Strong Technical Domains

🛠 Key Matched Skills

📄 Resume length insights

🎯 5. Recruiter Dashboard

Upload multiple resumes (PDF)

Filter candidates by minimum score

Shortlist candidates

Remove from shortlist

Export ranking report (CSV)

📈 6. Analytics Panel

Displays:

Total resumes processed

Average match score

Highest match score

Ranking system (🥇🥈🥉)

🛠 Tech Stack
Frontend & UI

Streamlit

NLP & AI

spaCy (Named Entity Recognition)

Sentence-Transformers

Scikit-learn

Data Processing

Pandas

NumPy

PDF Processing

PyPDF2

Visualization

Matplotlib

📂 Project Structure
AI-Resume-Screener/
│
├── src/
│   ├── main.py              # Streamlit Application
│   ├── matcher.py           # Resume ranking logic
│   ├── preprocess.py        # Text cleaning utilities
│   ├── skills.json          # Master skill database
│
├── requirements.txt
├── README.md

⚙️ Installation Guide (Run Locally)
1️⃣ Clone the Repository
git clone https://github.com/your-username/AI-Resume-Screener.git
cd AI-Resume-Screener

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Download spaCy Model
python -m spacy download en_core_web_sm

4️⃣ Run the Application
streamlit run src/main.py

☁️ Deployment (Streamlit Cloud)

Push your project to GitHub

Visit 👉 https://streamlit.io/cloud

Click New App

Select your repository

Set:

Branch: main

File path: src/main.py

Click Deploy

Your app will be live within minutes 🚀

🎯 Real-World Use Cases

✔ HR Resume Screening
✔ Campus Placement Filtering
✔ Internship Candidate Shortlisting
✔ Automated Technical Screening
✔ Resume Skill Gap Analysis

🔒 Security & Privacy

Resumes processed in memory

No permanent file storage

No external API sharing

Safe for local and cloud deployment

📌 Future Enhancements

Weighted skill scoring

Domain-specific scoring system

Resume improvement suggestions

Recruiter login system

Resume comparison dashboard

Database integration (PostgreSQL)

Admin analytics panel

Email-based candidate report

📊 Sample Output Preview

🥇 Ranked Candidate List

Skill Match Percentage

Missing Skills Breakdown

AI Resume Summary

CSV Downloadable Report

💡 Why This Project Is Strong

This project demonstrates:

✔ NLP
✔ Machine Learning
✔ Real-world application
✔ Full-stack thinking
✔ Deployment knowledge
✔ Recruiter-focused UX design

Perfect for:

AI/ML Internship

Software Engineering Role

Data Science Role

Product-based company applications

👨‍💻 Author

Ajay Kumar Singh
Final Year B.Tech Student
AI & Software Engineering Enthusiast

⭐ Support

If you found this project useful:

Star ⭐ the repository

Share it on LinkedIn

Fork and improve

📄 License

This project is open-source and available under the MIT License.