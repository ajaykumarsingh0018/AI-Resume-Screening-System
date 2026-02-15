from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def rank_resumes(resume_list, job_text):
    documents = resume_list + [job_text]
    embeddings = model.encode(documents, normalize_embeddings=True)

    job_embedding = embeddings[-1].reshape(1, -1)
    resume_embeddings = embeddings[:-1]

    similarities = cosine_similarity(resume_embeddings, job_embedding)

    scores = [float(score[0] * 100) for score in similarities]

    return scores

def extract_top_skills(job_text):
    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorizer = TfidfVectorizer(stop_words='english', max_features=15)
    X = vectorizer.fit_transform([job_text])

    return vectorizer.get_feature_names_out()

def match_resume(resume_text, job_text):
    embeddings = model.encode([resume_text, job_text], normalize_embeddings=True)

    similarity = cosine_similarity(
        embeddings[0].reshape(1, -1),
        embeddings[1].reshape(1, -1)
    )

    return float(similarity[0][0] * 100)

def recommend_jobs(resume_text):
    
    job_roles = {
        "Machine Learning Engineer":
        "Python machine learning deep learning NLP TensorFlow PyTorch data science model training",
        
        "Data Analyst":
        "SQL Excel Power BI data visualization statistics dashboards reporting data cleaning",
        
        "Full Stack Developer":
        "HTML CSS JavaScript React Node.js API backend frontend database MongoDB",
        
        "Cybersecurity Analyst":
        "network security penetration testing ethical hacking firewalls SIEM vulnerability assessment"
    }

    job_names = list(job_roles.keys())
    job_descriptions = list(job_roles.values())

    documents = [resume_text] + job_descriptions

    embeddings = model.encode(documents, normalize_embeddings=True)

    resume_embedding = embeddings[0].reshape(1, -1)
    job_embeddings = embeddings[1:]

    similarities = cosine_similarity(resume_embedding, job_embeddings)[0]

    results = list(zip(job_names, similarities * 100))
    results.sort(key=lambda x: x[1], reverse=True)

    return results[:3]

