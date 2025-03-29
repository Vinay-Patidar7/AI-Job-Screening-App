import streamlit as st
from auth import login, signup
from recruiter import recruiter_dashboard
from candidate import candidate_dashboard

st.set_page_config(page_title="AI Job Screening", layout="wide")

if "username" not in st.session_state:
    st.session_state["username"] = None
    st.session_state["role"] = None

if not st.session_state["username"]:
    st.sidebar.title("Authentication")
    auth_choice = st.sidebar.radio("Choose", ["Login", "Sign Up"])
    
    if auth_choice == "Login":
        login()
    else:
        signup()
else:
    st.sidebar.title(f"Welcome, {st.session_state['username']} ({st.session_state['role']})")
    if st.sidebar.button("Logout"):
        st.session_state["username"] = None
        st.session_state["role"] = None
        st.rerun()

    if st.session_state["role"] == "recruiter":
        recruiter_dashboard()
    elif st.session_state["role"] == "candidate":
        candidate_dashboard()
