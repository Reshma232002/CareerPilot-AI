import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

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
# RESUME ANALYSIS
# ==================================================
def resume_analysis():

    reset_daily_usage_if_needed(st.session_state.user_email)

    st.markdown("## 📄 Resume Analyzer")
    st.caption("Upload your resume and compare it with a Job Description using AI.")

    uploaded_file = st.file_uploader(
        "📂 Upload Resume (PDF)",
        type=["pdf"]
    )

    job_description = st.text_area(
        "💼 Paste Job Description",
        height=180,
        placeholder="Paste the complete Job Description here..."
    )


    if uploaded_file and job_description.strip():

        allowed, message = can_use_service(st.session_state.user_email)

        if not allowed:
            st.error(message)
            st.stop()

        resume_text = extract_text_from_pdf(uploaded_file)

        st.subheader("Extracted Resume")
        st.text_area("Resume Text", resume_text, height=250)

        result = analyze_resume(resume_text, job_description)

        gemini_output = generate_ai_content(resume_text, job_description)

        st.subheader("Gemini AI Insights")
        st.markdown(gemini_output)

        score = int(result["score"])

        st.divider()

        st.markdown("## ⭐ Resume Match Score")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Overall ATS Score", f"{score}/100")

        with col2:
            if score >= 80:
                st.success("Excellent Match")
            elif score >= 60:
                st.warning("Good Match")
            else:
                st.error("Needs Improvement")

        with col3:
            st.metric("Matched Skills", len(result["matched"]))

        st.progress(score / 100)
        # ==========================================
        # TABS
        # ==========================================
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Skills",
            "🤖 AI Insights",
            "📝 Cover Letter",
            "💼 LinkedIn",
            "🎤 Interview"
        ])

        # ==========================================
        # Skills
        # ==========================================
        with tab1:

            col1, col2 = st.columns(2)

            with col1:
                st.subheader("✅ Matched Skills")

                if result["matched"]:
                    for skill in result["matched"]:
                        st.success(skill)
                else:
                    st.info("No matched skills found.")

            with col2:
                st.subheader("❌ Missing Skills")

                if result["missing"]:
                    for skill in result["missing"]:
                        st.error(skill)
                else:
                    st.success("No missing skills!")

        # ==========================================
        # AI Insights
        # ==========================================
        with tab2:

            st.subheader("🤖 AI Career Suggestions")
            st.info(gemini_output)

        # ==========================================
        # Cover Letter
        # ==========================================
        with tab3:

            st.text_area(
                "Generated Cover Letter",
                result["cover_letter"],
                height=300
            )

            st.download_button(
                "📥 Download Cover Letter",
                data=result["cover_letter"],
                file_name="cover_letter.txt"
            )

        # ==========================================
        # LinkedIn
        # ==========================================
        with tab4:

            st.text_area(
                "LinkedIn Summary",
                result["linkedin_summary"],
                height=250
            )

        # ==========================================
        # Interview Questions
        # ==========================================
        with tab5:

            for i, question in enumerate(result["interview_questions"], 1):

                with st.expander(f"Question {i}", expanded=(i == 1)):
                    st.write(question)

        # ==========================================
        # PDF REPORT
        # ==========================================
        pdf_path = "resume_report.pdf"

        generate_pdf(
            pdf_path,
            result["score"],
            result["matched"],
            result["missing"],
            result["cover_letter"],
            result["linkedin_summary"],
            gemini_output,
        )

        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                "📥 Download Full AI Report (PDF)",
                data=pdf_file,
                file_name="AI_Resume_Report.pdf",
                mime="application/pdf",
            )

        # ==========================================
        # SAVE ANALYSIS
        # ==========================================
        if st.button("💾 Save Analysis", use_container_width=True):

            save_analysis(
                user_email=st.session_state.user_email,
                resume_text=resume_text,
                job_description=job_description,
                ats_score=result["score"],
                matched_skills=result["matched"],
                missing_skills=result["missing"],
                cover_letter=result["cover_letter"],
                linkedin_summary=result["linkedin_summary"],
                ai_insights=gemini_output,
            )

            increment_usage(st.session_state.user_email)

            st.success("✅ Analysis saved successfully!")


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
