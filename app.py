import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
from pages.resume_analyzer import resume_analysis

from firebase_config import auth
from pdf_utils import extract_text_from_pdf
from ai_engine import analyze_resume
from gemini_engine import generate_ai_content
from pdf_generator import generate_pdf
from user_plan import can_use_service
from backend_db import (
    increment_usage,
    save_analysis,
    get_user_history,
    get_dashboard_stats,
    reset_daily_usage_if_needed,
    create_user_if_not_exists
)

from payment import create_order, verify_payment, upgrade_user


# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
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
# DASHBOARD
# ==================================================
def dashboard():
    st.info(
    """
    ### 👋 Welcome to CareerPilot AI

    Your personal AI career assistant.

    ✔ Resume Analysis

    ✔ ATS Optimization

    ✔ Interview Coach

    ✔ Career Roadmaps

    ✔ AI Copilot
    """
    )
    reset_daily_usage_if_needed(st.session_state.user_email)

    st.markdown("# 🚀 Dashboard")

    st.caption("Welcome back to CareerPilot AI")

    st.divider()

    stats = get_dashboard_stats(st.session_state.user_email)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📄 Total Analyses",
            stats.get("total", 0)
        )

    with col2:
        st.metric(
            "⭐ Average ATS",
            f"{stats.get('avg_score',0)}%"
        )

    with col3:
        st.metric(
            "🏆 Best Score",
            f"{stats.get('max_score',0)}%"
        )

    history = get_user_history(st.session_state.user_email)

    if history:
        df = pd.DataFrame([
            {"Analysis": i + 1, "ATS Score": item.get("ats_score", 0)}
            for i, item in enumerate(history)
        ])

        fig = px.line(df, x="Analysis", y="ATS Score", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No analyses yet.")


# ==================================================



    st.button("Logout", on_click=logout)

# ==================================================
# JOB MATCHER
# ==================================================
def job_matcher():

    st.subheader("🎯 Job Matcher")

    st.info("Coming Soon")

    st.write(
        """
        Future Features:
        - Match resume with jobs
        - ATS compatibility
        - Skill gap analysis
        - AI recommendations
        """
    )
# ==================================================
# INTERVIEW COACH
# ==================================================
def interview_coach():

    st.subheader("🎤 Interview Coach")

    st.info("Coming Soon")

    st.write(
        """
        Future Features:
        - Mock interviews
        - Technical questions
        - HR questions
        - AI feedback
        """
    )
# ==================================================
# CAREER COACH
# ==================================================
def career_coach():

    st.subheader("🚀 Career Coach")

    st.info("Coming Soon")

    st.write(
        """
        Future Features:
        - Career roadmap
        - Skill recommendations
        - Salary guidance
        - Learning path generation
        """
    )        
# ==================================================
# HISTORY
# ==================================================
def analysis_history():

    st.subheader("Previous Analyses")

    history = get_user_history(st.session_state.user_email)

    if history:
        for i, item in enumerate(history, 1):

            with st.expander(f"Analysis {i} | ATS: {item.get('ats_score', 0)}"):

                st.metric("ATS Score", f"{item.get('ats_score', 0)} / 100")
                st.write("Matched:", item.get("matched_skills", []))
                st.write("Missing:", item.get("missing_skills", []))

                st.text_area("Cover Letter", item.get("cover_letter", ""), key=f"cl_{i}")
                st.text_area("LinkedIn", item.get("linkedin_summary", ""), key=f"li_{i}")

                st.markdown(item.get("ai_insights", ""))

    else:
        st.info("No saved analyses.")


# ==================================================
# LOGIN / SIGNUP
# ==================================================
def login_signup():

    menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if menu == "Sign Up":

        if st.button("Sign Up"):
            try:
                auth.create_user_with_email_and_password(email, password)
                create_user_if_not_exists(email)
                st.success("Account created!")
            except Exception as e:
                st.error(e)

    else:

        if st.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)

                st.session_state.user = user
                st.session_state.user_email = email

                create_user_if_not_exists(email)

                st.success("Login successful!")
                st.rerun()

            except Exception as e:
                st.error(f"Login failed: {str(e)}")

            st.sidebar.success(f"👋 {st.session_state.user_email}")

            st.sidebar.write("CareerPilot AI")
# ==================================================
# MAIN APP
# ==================================================
if st.session_state.user:

    st.success(f"Logged in as: {st.session_state.user_email}")

    if st.sidebar.button("Logout"):
        logout()

        st.sidebar.markdown("## 🚀 CareerPilot AI")

        st.sidebar.success(f"👤 {st.session_state.user_email}")

        st.sidebar.divider()

        page = st.sidebar.radio(
                "📂 Navigation",
            [
                "🏠 Dashboard",
                "📄 Resume Analyzer",
                "📊 Analysis History",
                "🤖 AI Copilot",
                "💰 Pricing",
                "⚙ Settings"
            ]
        )

        if page == "🏠 Dashboard":
            dashboard()

        elif page == "📄 Resume Analyzer":
            resume_analysis()

        elif page == "📊 Analysis History":
            analysis_history()

        elif page == "🤖 AI Copilot":
            st.switch_page("pages/AI_Copilot.py")

        elif page == "⚙ Settings":
            st.switch_page("pages/Settings.py")

        elif page == "💰 Pricing":

            col1, col2, col3 = st.columns(3)

        # ================= FREE =================
        with col1:
            st.info("Free: 1 analysis/day")

        # ================= PREMIUM =================
        with col2:
            st.success("Premium ₹99/month")

            if st.button("Pay ₹99 Premium"):

                order = create_order(99)

                st.session_state.premium_order = order["id"]

                checkout_html = f"""
                <script src="https://checkout.razorpay.com/v1/checkout.js"></script>

                <script>
                var options = {{
                    "key": "{st.secrets["RAZORPAY_KEY_ID"]}",
                    "amount": "9900",
                    "currency": "INR",
                    "order_id": "{order['id']}",
                    "handler": function (response) {{
                        window.parent.postMessage(response, "*");
                    }}
                }};
                var rzp = new Razorpay(options);
                rzp.open();
                </script>
                """

                components.html(checkout_html, height=600)

            if st.session_state.premium_order:

                st.write("Enter payment details:")

                o = st.text_input("Order ID")
                p = st.text_input("Payment ID")
                s = st.text_input("Signature")

                if st.button("Verify Premium Payment"):

                    if verify_payment(o, p, s):
                        upgrade_user(st.session_state.user_email, "premium")
                        st.success("Premium Activated!")
                        st.session_state.premium_order = None
                        st.rerun()
                    else:
                        st.error("Payment failed")

        # ================= RECRUITER =================
        with col3:
            st.warning("Recruiter ₹299/month")

            if st.button("Pay ₹299 Recruiter"):

                order = create_order(299)

                st.session_state.recruiter_order = order["id"]

                checkout_html = f"""
                <script src="https://checkout.razorpay.com/v1/checkout.js"></script>

                <script>
                var options = {{
                    "key": "{st.secrets["RAZORPAY_KEY_ID"]}",
                    "amount": "29900",
                    "currency": "INR",
                    "order_id": "{order['id']}",
                    "handler": function (response) {{
                        window.parent.postMessage(response, "*");
                    }}
                }};
                var rzp = new Razorpay(options);
                rzp.open();
                </script>
                """

                components.html(checkout_html, height=600)

            if st.session_state.recruiter_order:

                st.write("Enter payment details:")

                o = st.text_input("Order ID Recruiter")
                p = st.text_input("Payment ID Recruiter")
                s = st.text_input("Signature Recruiter")

                if st.button("Verify Recruiter Payment"):

                    if verify_payment(o, p, s):
                        upgrade_user(st.session_state.user_email, "recruiter")
                        st.success("Recruiter Activated!")
                        st.session_state.recruiter_order = None
                        st.rerun()
                    else:
                        st.error("Payment failed")

else:
    login_signup()
