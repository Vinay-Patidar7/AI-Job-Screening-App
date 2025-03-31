import ollama
from preprocess import extract_text_from_pdf

def analyze_resume_with_ollama(resume_path, job_title, job_description):
    resume_text = extract_text_from_pdf(resume_path)

    prompt = f"""
    You are an AI-based job screening system.
    Here is the **Job Role**: {job_title}
    Here is the **Job Description**: {job_description}

    Now, evaluate this **Candidate Resume**:
    {resume_text}

    Based on this resume, should the candidate be shortlisted? Provide a clear response as:
    - "Shortlisted" if the resume matches the job description.
    - "Not Shortlisted" if the resume does not match.
    Also, briefly justify your answer.
    """

    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

if __name__ == "__main__":
    print(analyze_resume_with_ollama("../data/resumes/C1061.pdf", "Data Scientist", "Looking for a candidate with NLP & Python skills"))
