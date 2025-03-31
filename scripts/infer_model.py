import pickle
from preprocess import extract_text_from_pdf, vectorize_text
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Absolute Paths
model_path = "/Users/vinaypatidar/Desktop/Accenture Hacakthon/job_screening/models/resume_match_model.pkl"
vectorizer_path = "/Users/vinaypatidar/Desktop/Accenture Hacakthon/job_screening/models/job_vectorizer.pkl"
resume_path = "/Users/vinaypatidar/Desktop/Accenture Hacakthon/job_screening/data/resumes/one.pdf"

# Load trained model and vectorizer
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")
if not os.path.exists(vectorizer_path):
    raise FileNotFoundError(f"Vectorizer file not found at {vectorizer_path}")

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(vectorizer_path, "rb") as f:
    vectorizer = pickle.load(f)

# Set minimum accuracy requirement
REQUIRED_ACCURACY = 80.0  # 80% threshold

# Ensure vector dimensions match training
def predict_resume_match(resume_path, job_description, model_accuracy):
    resume_text = extract_text_from_pdf(resume_path)
    
    # Convert texts to vectors
    resume_vector = vectorizer.transform([resume_text])
    job_vector = vectorizer.transform([job_description])
    
    # Check feature size match
    if resume_vector.shape[1] != model.n_features_in_:
        raise ValueError(f"Mismatch in feature size. Model expects {model.n_features_in_}, but got {resume_vector.shape[1]}")

    # Predict using trained model
    prediction = model.predict(resume_vector.toarray())[0]
    
    # Calculate match score (cosine similarity)
    match_score = cosine_similarity(resume_vector, job_vector)[0][0] * 100  # Percentage format
    
    # **NEW CONDITION:** Check if model accuracy is >= 80%
    if model_accuracy >= REQUIRED_ACCURACY:
        if prediction == 1:
            return f"✅ Resume matches the job! (Match Score: {match_score:.2f}%)"
        else:
            return f"❌ Resume does not match. (Match Score: {match_score:.2f}%)"
    else:
        return f"⚠ Model accuracy too low ({model_accuracy:.2f}%). Cannot determine match."

if __name__ == "__main__":
    job_description =  """We are seeking a skilled Software Engineer to design, develop, and maintain software applications. 
    The ideal candidate will write efficient code, troubleshoot issues, and collaborate with teams to deliver high-quality solutions.
    Responsibilities:
    - Develop, test, and deploy software applications.
    - Write clean, maintainable, and scalable code.
    - Collaborate with cross-functional teams to define and implement features.
    - Troubleshoot and debug issues for optimal performance.
    - Stay updated with emerging technologies and best practices.
    Qualifications:
    - Bachelor's degree in Computer Science or a related field.
    - Proficiency in programming languages like Python, Java, or C++.
    - Experience with databases, web development, and software frameworks.
    - Strong problem-solving skills and attention to detail.
    - Ability to work both independently and in a team environment."""
    model_accuracy = 90.0  # Replace this with the printed accuracy from train_model.py
    result = predict_resume_match(resume_path, job_description, model_accuracy)
    print(result)
