import streamlit as st
import sqlite3

def get_jobs():
    """Fetch all job postings from the database"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description FROM jobs")
    jobs = cursor.fetchall()
    conn.close()
    return jobs

def job_listings():
    """Display job openings in boxes with an Apply button"""
    st.title("Job Openings")

    jobs = get_jobs()

    if not jobs:
        st.info("No job openings available at the moment.")
        return

    for job in jobs:
        job_id, title, description = job

        # Create a container (box) for each job posting
        with st.container():
            st.subheader(title)
            st.write(description)
            
            # Apply Button
            if st.button(f"Apply for {title}", key=f"apply_{job_id}"):
                apply_for_job(job_id)

        st.markdown("---")  # Add a separator line between jobs

def apply_for_job(job_id):
    """Apply for a job using the stored resume"""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Check if the candidate has uploaded a resume
    cursor.execute("SELECT resume_file FROM resumes WHERE username=?", (st.session_state["username"],))
    resume = cursor.fetchone()

    if resume and resume[0]:
        # Insert application into the applications table
        cursor.execute("INSERT INTO applications (username, job_id, resume_file) VALUES (?, ?, ?)", 
                       (st.session_state["username"], job_id, resume[0]))
        conn.commit()
        st.success(f"Successfully applied for {job_id}!")
    else:
        st.error("You haven't uploaded a resume. Please upload your resume first.")

    conn.close()

def upload_resume():
    """Allow candidates to upload their resume as a PDF file"""
    st.title("Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
    
    if uploaded_file is not None:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("REPLACE INTO resumes (username, resume_file) VALUES (?, ?)", 
                       (st.session_state["username"], uploaded_file.read()))
        conn.commit()
        conn.close()
        st.success("Resume uploaded successfully!")

def candidate_dashboard():
    """Main Candidate Dashboard with Job Listings"""
    st.sidebar.title("Candidate Menu")
    page = st.sidebar.radio("Navigate", ["Job Openings", "Upload Resume"])

    if page == "Job Openings":
        job_listings()
    elif page == "Upload Resume":
        upload_resume()
