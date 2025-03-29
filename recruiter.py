import streamlit as st
from database import insert_job, get_jobs, get_applicants

def recruiter_dashboard():
    st.title("Recruiter Dashboard")

    st.subheader("Post a Job")
    job_title = st.text_input("Job Title")
    job_description = st.text_area("Job Description")
    if st.button("Post Job"):
        insert_job(job_title, job_description, st.session_state["username"])
        st.success("Job posted successfully!")

    st.subheader("Applicants for Your Jobs")
    jobs = get_jobs()
    for job in jobs:
        if job[2] == st.session_state["username"]:
            st.write(f"### {job[1]}")
            applicants = get_applicants(job[0])
            for applicant in applicants:
                st.write(f"- {applicant[0]} | Score: {applicant[1]}")
