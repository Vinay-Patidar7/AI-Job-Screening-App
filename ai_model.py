import ollama

def analyze_resume(job_description, resume_text):
    prompt = f"""
    Job Description:
    {job_description}

    Candidate Resume:
    {resume_text}

    Based on the job description, score the candidate's suitability from 0 to 10.
    Provide a short reasoning.
    """
    
    response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
    
    return response["message"]["content"]
