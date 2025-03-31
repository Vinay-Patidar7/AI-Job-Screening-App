import streamlit as st
from database import insert_job, get_jobs_by_recruiter, get_applicants, get_resume

def recruiter_dashboard():
    st.title("Recruiter Dashboard")

    # ✅ Post a Job
    st.subheader("Post a Job")
    job_title = st.text_input("Job Title")
    job_description = st.text_area("Job Description")
    if st.button("Post Job"):
        insert_job(job_title, job_description, st.session_state["username"])
        st.success("Job posted successfully!")

    # ✅ Show Previously Posted Jobs
    st.subheader("Your Job Postings")
    jobs = get_jobs_by_recruiter(st.session_state["username"])

    if not jobs:
        st.write("You haven't posted any jobs yet.")
    else:
        for job in jobs:
            job_id, title, description = job
            st.write(f"### {title}")
            st.write(description)

            # ✅ Show Applicants for This Job
            applicants = get_applicants(job[0])  # Fetch applicants for the job

            if applicants:
                st.write("### Applicants:")
            for username, resume_file in applicants:
                st.write(f"**Username:** {username}")
                        
                        # Resume download button
                if resume_file:
                    st.download_button(
                        label="Download Resume",
                        data=resume_file,
                        file_name=f"{username}_resume.pdf",
                        mime="application/pdf",
                        key=f"download_{job_title}_{username}"  # Ensure uniqueness
                    )
                else:
                    st.write("No applicants yet.")