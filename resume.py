import streamlit as st
import sqlite3

def save_resume(username, name, email, phone, skills, experience, education):
    """Saves the resume to the database."""
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO resumes (username, name, email, phone, skills, experience, education) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (username, name, email, phone, skills, experience, education))
    
    conn.commit()
    conn.close()

def create_resume():
    """Candidate Resume Creation Page"""
    st.title("Create Your Resume")

    if "username" not in st.session_state:
        st.error("Please log in to create a resume.")
        return

    username = st.session_state["username"]

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    skills = st.text_area("Skills (comma-separated)")
    experience = st.text_area("Work Experience")
    education = st.text_area("Education")

    if st.button("Save Resume"):
        if name and email and phone and skills and experience and education:
            save_resume(username, name, email, phone, skills, experience, education)
            st.success("Resume saved successfully!")
        else:
            st.warning("Please fill in all fields.")
