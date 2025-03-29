import streamlit as st
from database import insert_user, check_user

def login():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        role = check_user(username, password)
        if role:
            st.session_state["username"] = username
            st.session_state["role"] = role
            st.success(f"Logged in as {role}")
            st.rerun()  # ✅ Fixed: Use st.rerun() instead of st.experimental_rerun()
        else:
            st.error("Invalid credentials!")

def signup():
    st.subheader("Sign Up")
    username = st.text_input("New Username")
    password = st.text_input("New Password", type="password")
    role = st.selectbox("Select Role", ["recruiter", "candidate"])
    
    if st.button("Sign Up"):
        if insert_user(username, password, role):
            st.success("Account created! Please login.")
        else:
            st.error("Username already exists!")
