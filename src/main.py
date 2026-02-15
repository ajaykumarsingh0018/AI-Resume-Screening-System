import streamlit as st
import PyPDF2
from matcher import rank_resumes
from preprocess import clean_text
from matcher import recommend_jobs
import pandas as pd
import json
import os
import re
import matplotlib.pyplot as plt
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    entities = []

    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT"]:
            if len(ent.text) > 2:
                entities.append(ent.text.lower())

    return list(set(entities))




st.title("AI Resume Screening System")
if "shortlisted" not in st.session_state:
    st.session_state.shortlisted = []


uploaded_files = st.file_uploader(
    "Upload Resumes",
    accept_multiple_files=True,
    type=["pdf"]
)

job_desc = st.text_area("Paste Job Description")


# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text

def detect_skills(text, skill_list):
    detected = []
    for skill in skill_list:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            detected.append(skill)
    return detected

def generate_resume_summary(resume_text, matched_skills, job_skills):
    summary = ""

    # Basic length-based experience guess
    word_count = len(resume_text.split())

    if word_count > 1500:
        level = "Senior Level Candidate"
    elif word_count > 800:
        level = "Mid Level Candidate"
    else:
        level = "Entry Level Candidate"

    summary += f"📌 Profile Level: {level}\n\n"

    if matched_skills:
        summary += "💼 Key Technical Strengths:\n"
        summary += ", ".join(sorted(matched_skills)) + "\n\n"
    else:
        summary += "⚠ Limited matching technical skills detected.\n\n"

    summary += f"📄 Resume Length: {word_count} words\n"

    return summary


if uploaded_files and job_desc.strip():


    BASE_DIR = os.path.dirname(__file__)
    skills_path = os.path.join(BASE_DIR, "skills.json")

    with open(skills_path, "r") as f:
        MASTER_SKILLS = json.load(f)


    if len(job_desc.split()) < 20:
        st.warning("Please enter at least 20 words in job description.")
        st.stop()

    cleaned_job = clean_text(job_desc)

    results = []

    # Process all resumes first
    for resume_file in uploaded_files:

        try:
            resume_text = extract_text_from_pdf(resume_file)
        except Exception:
            st.error(
                f"{resume_file.name} may be a scanned/image PDF. "
                "Please upload a text-based PDF."
            )
            continue

        cleaned_resume = clean_text(resume_text)

        scores = rank_resumes([cleaned_resume], cleaned_job)
        if not scores:
            continue

        score = scores[0]
        
        results.append((resume_file.name, score, cleaned_resume, resume_text))
    
        
    # Sort by highest score
    results.sort(key=lambda x: x[1], reverse=True)
    total_resumes = len(results)
    average_score = sum([r[1] for r in results]) / total_resumes if total_resumes > 0 else 0
    highest_score = results[0][1] if total_resumes > 0 else 0

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Resumes", total_resumes)
    col2.metric("Average Match Score", f"{average_score:.2f}%")
    col3.metric("Top Match Score", f"{highest_score:.2f}%")

    st.subheader("🎯 Filter Candidates")
    min_score = st.slider("Minimum Match Score", 0, 100, 0)

    if results:
        top_name, top_score, _, _ = results[0]

        st.subheader("🏆 Top Candidate")
        st.success(f"{top_name} — {top_score:.2f}% Match")
    
    if not results:
        st.warning("No valid resumes processed.")
        st.stop()


    df = pd.DataFrame(results, columns=["Resume Name", "Score", "Cleaned Text", "Raw Text"])
    df = df[["Resume Name", "Score"]]


    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Ranking Report",
        csv,
        "resume_ranking.csv",
        "text/csv",
        key="download_csv_button"
    )

    st.header("📊 Resume Ranking Results")

    json_skills = detect_skills(cleaned_job, MASTER_SKILLS)
    ner_skills = extract_entities(job_desc)
    job_skills = list(set(json_skills + ner_skills))

    for index, (name, score, cleaned_resume, resume_text) in enumerate(results):

        if score < min_score:
            continue

        if index == 0:
            st.markdown("### 🥇 Ranked #1 Candidate")
        elif index == 1:
            st.markdown("### 🥈 Ranked #2 Candidate")
        elif index == 2:
            st.markdown("### 🥉 Ranked #3 Candidate")
        else:
            st.markdown(f"### 🔹 Ranked #{index+1} Candidate")


        st.subheader(name)
        st.write(f"Match Score: {score:.2f}%")
        progress_value = max(0, min(100, int(score)))
        st.progress(progress_value)


        if score > 75:
            st.success("Excellent Match 🚀")
        elif score > 50:
            st.warning("Moderate Match ⚠")
        else:
            st.error("Low Match ❌")

        if st.button(f"Shortlist {name}", key=f"shortlist_{index}_{name}"):
            if name not in [c[0] for c in st.session_state.shortlisted]:
                st.session_state.shortlisted.append((name, score))
                st.success(f"{name} added to shortlist!")


        # Job Recommendations
        recommendations = recommend_jobs(cleaned_resume)

        with st.expander("🔎 View Detailed Analysis"):
            # Job Recommendations
            st.subheader("🤖 AI Job Recommendations")
            for job, rec_score in recommendations:
                st.write(f"{job} — {rec_score:.2f}% match")

            # Skill Analysis
            resume_json_skills = detect_skills(cleaned_resume, MASTER_SKILLS)
            resume_ner_skills = extract_entities(resume_text)
            resume_skills = list(set(resume_json_skills + resume_ner_skills))

            matched_skills = list(set(job_skills) & set(resume_skills))
            missing_skills = list(set(job_skills) - set(resume_skills))

            if job_skills:
                skill_match_percentage = (len(matched_skills) / len(job_skills)) * 100
            else:
                skill_match_percentage = 0

            st.subheader("📈 Skill Match Percentage")
            st.write(f"{skill_match_percentage:.2f}% Skills Matched")
            st.progress(skill_match_percentage / 100)

            st.subheader("✅ Matched Skills")
            if matched_skills:
                st.success(", ".join(sorted(matched_skills)))
            else:
                st.warning("No required skills matched.")

            st.subheader("🔎 Missing Skills")
            if missing_skills:
                st.error(", ".join(sorted(missing_skills)))
            else:
                st.success("No major technical skills missing 🎉")
            
            with st.expander("🧠 AI Resume Summary", expanded=False):
                summary = generate_resume_summary(resume_text, matched_skills, job_skills)
                st.info(summary)


    
    if st.session_state.shortlisted:
        st.subheader("📌 Shortlisted Candidates")

        for candidate, score in st.session_state.shortlisted:

            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(f"{candidate} — {score:.2f}%")

            with col2:
                if st.button("Remove", key=f"remove_{candidate}"):
                    st.session_state.shortlisted = [
                        c for c in st.session_state.shortlisted
                        if c[0] != candidate
                    ]
                    st.success(f"{candidate} removed from shortlist!")
                    st.rerun()
