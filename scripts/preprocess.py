import pandas as pd
import PyPDF2
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import chardet

# Detect file encoding
def detect_encoding(file_path):
    with open(file_path, "rb") as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
        return result['encoding']

# Load job descriptions
def load_job_descriptions(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Job description file not found at {csv_path}")
    encoding = detect_encoding(csv_path)
    df = pd.read_csv(csv_path, encoding=encoding)
    return df[['Job Title', 'Job Description']]

# Extract text from PDFs (resumes)
def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"Resume file not found at {pdf_path}")
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

# Process resumes in a folder
def process_resumes(resume_folder):
    if not os.path.exists(resume_folder):
        raise FileNotFoundError(f"Resume folder not found at {resume_folder}")
    resumes = []
    for file in os.listdir(resume_folder):
        if file.endswith(".pdf"):
            resume_text = extract_text_from_pdf(os.path.join(resume_folder, file))
            resumes.append({'Filename': file, 'Text': resume_text})
    return pd.DataFrame(resumes)

# Convert text data into TF-IDF features
def vectorize_text(texts):
    vectorizer = TfidfVectorizer(stop_words="english", max_features=2000)
    return vectorizer.fit(texts)

if __name__ == "__main__":
    job_csv_path = "/Users/vinaypatidar/Desktop/Accenture Hacakthon/job_screening/data/job_description.csv"
    resume_folder = "/Users/vinaypatidar/Desktop/Accenture Hacakthon/job_screening/data/resumes"
    
    job_data = load_job_descriptions(job_csv_path)
    resume_data = process_resumes(resume_folder)
    
    job_texts = job_data["Job Description"].tolist()
    resume_texts = resume_data["Text"].tolist()
    
    vectorizer = vectorize_text(job_texts + resume_texts)
    print("✅ Preprocessing Complete!")
