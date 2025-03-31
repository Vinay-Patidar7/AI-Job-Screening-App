import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import vectorize_text, load_job_descriptions, process_resumes
from sklearn.model_selection import cross_val_score
import time
# Absolute Paths
job_csv_path = "/Users/vinaypatidar/Desktop/Accenture Hacakthon/job_screening/data/job_description.csv"
resume_folder = "/Users/vinaypatidar/Desktop/Accenture Hacakthon/job_screening/data/resumes"
model_path = "/Users/vinaypatidar/Desktop/Accenture Hacakthon/job_screening/models/resume_match_model.pkl"
vectorizer_path = "/Users/vinaypatidar/Desktop/Accenture Hacakthon/job_screening/models/job_vectorizer.pkl"

# Load processed data
job_data = load_job_descriptions(job_csv_path)
resume_data = process_resumes(resume_folder)

job_texts = job_data["Job Description"].tolist()
resume_texts = resume_data["Text"].tolist()

# Convert text to numerical format
vectorizer = vectorize_text(job_texts + resume_texts)
job_vectors = vectorizer.transform(job_texts)
resume_vectors = vectorizer.transform(resume_texts)

# Generate labels using cosine similarity
similarity_scores = cosine_similarity(resume_vectors, job_vectors).max(axis=1)
y = [1 if score > 0.7 else 0 for score in similarity_scores]  # Threshold-based labeling

# Train the model
X_train, X_test, y_train, y_test = train_test_split(resume_vectors.toarray(), y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=300, max_depth=10, min_samples_split=5, random_state=42)

model.fit(X_train, y_train)

scores = cross_val_score(model, X_train, y_train, cv=5)
print(f"Cross-validation accuracy: {scores.mean() * 100:.2f}%")

# Save the trained model and vectorizer
with open(model_path, "wb") as f:
    pickle.dump(model, f)

with open(vectorizer_path, "wb") as f:
    pickle.dump(vectorizer, f)

accuracy = model.score(X_test, y_test) * 100
print(f"🎯 Model Accuracy: {accuracy:.2f}%")
print("✅ Model Training Complete!")

start_time = time.time()
model.fit(X_train, y_train)
print(f"Training Time: {time.time() - start_time:.2f} sec")