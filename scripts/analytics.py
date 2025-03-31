import streamlit as st
import sqlite3
import pandas as pd

def fetch_statistics():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Total jobs and applications
    cursor.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM applications")
    total_applications = cursor.fetchone()[0]
    
    # Top skills in resumes
    cursor.execute("SELECT skills FROM resumes")
    skills_data = cursor.fetchall()
    
    skill_counts = {}
    for row in skills_data:
        skills = row[0].split(',')
        for skill in skills:
            skill = skill.strip()
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

    top_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    conn.close()
    return total_jobs, total_applications, top_skills

def show_analytics():
    st.title("AI Job Screening Analytics")

    total_jobs, total_applications, top_skills = fetch_statistics()

    st.metric("Total Job Listings", total_jobs)
    st.metric("Total Applications", total_applications)

    st.subheader("Top In-Demand Skills")
    for skill, count in top_skills:
        st.write(f"**{skill}** - {count} resumes")

if __name__ == "__main__":
    show_analytics()
