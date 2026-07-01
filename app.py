import streamlit as st
import streamlit.components.v1 as components

from firebase_config import auth
from backend_db import create_user_if_not_exists

# ---------- Import Pages ----------
from modules.dashboard import dashboard
from modules.resume_analyzer import resume_analysis
from modules.analysis_history import analysis_history
from modules.pricing import pricing
from modules.job_matcher import job_matcher
from modules.interview_coach import interview_coach
from modules.career_planner import career_planner
from modules.ai_copilot import ai_copilot
from modules.settings import settings


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)
with open("assets/styles.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
    
st.title("🚀 CareerPilot AI")
st.caption("Your AI Career Company")

# ==================================================
# SESSION STATE
# ==================================================

if "user" not in st.session_state:
    st.session_state.user = None

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "premium_order" not in st.session_state:
    st.session_state.premium_order = None

if "recruiter_order" not in st.session_state:
    st.session_state.recruiter_order = None

# ==================================================
# LOGOUT
# ==================================================

def logout():

    st.session_state.user = None
    st.session_state.user_email = ""
    st.session_state.premium_order = None
    st.session_state.recruiter_order = None

    st.rerun()

# ==================================================
# LOGIN / SIGNUP
# ==================================================

def login_signup():

    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Sign Up"]
    )

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if menu == "Sign Up":

        if st.button("Create Account"):

            try:

                auth.create_user_with_email_and_password(
                    email,
                    password
                )

                create_user_if_not_exists(email)

                st.success("Account created successfully!")

            except Exception as e:

                st.error(e)

    else:

        if st.button("Login"):

            try:

                user = auth.sign_in_with_email_and_password(
                    email,
                    password
                )

                st.session_state.user = user
                st.session_state.user_email = email

                create_user_if_not_exists(email)

                st.success("Login Successful")

                st.rerun()

            except Exception as e:

                st.error(f"Login Failed\n\n{e}")
    # ==================================================
# MAIN APPLICATION
# ==================================================

if st.session_state.user:

    # ---------------- Sidebar ----------------

    with st.sidebar:

        st.success(f"👋 {st.session_state.user_email}")

        st.markdown("---")

        page = st.radio(
            "📂 Navigation",
            [
                "🏠 Dashboard",
                "📄 Resume Analyzer",
                "🚀 Career Planner",
                "🎯 Job Matcher",
                "🎤 Interview Coach",
                "📊 Analysis History",
                "🤖 AI Copilot",
                "💰 Pricing",
                "⚙ Settings",
            ]
        )

        st.markdown("---")

        if st.button("🚪 Logout", use_container_width=True):
            logout()

    # ---------------- Routing ----------------

    if page == "🏠 Dashboard":

        dashboard()

    elif page == "📄 Resume Analyzer":

        resume_analysis()

    elif page == "🚀 Career Planner":

        career_planner()

    elif page == "🎯 Job Matcher":

        job_matcher()

    elif page == "🎤 Interview Coach":

        interview_coach()

    elif page == "📊 Analysis History":

        analysis_history()


    elif page == "🤖 AI Copilot":
        ai_copilot()

    elif page == "💰 Pricing":

        pricing()

    elif page == "⚙ Settings":

        settings()

else:

    login_signup()            
