import streamlit as st

from pdf_utils import extract_text_from_pdf
from ai_engine import analyze_resume
from gemini_engine import generate_ai_content
from pdf_generator import generate_pdf
from email_utils import send_email_with_attachment

from user_plan import can_use_service

from backend_db import (
    increment_usage,
    increment_feature_count,
    save_analysis,
    reset_daily_usage_if_needed,
    add_notification,
)


# ==================================================
# RESUME ANALYZER
# ==================================================
def resume_analysis():

    reset_daily_usage_if_needed(st.session_state.user_email)

    st.title(" Resume Analyzer")
    st.caption(
        "Upload your resume and compare it with a Job Description using AI."
    )

    uploaded_file = st.file_uploader(
        "📂 Upload Resume (PDF)",
        type=["pdf"]
    )

    job_description = st.text_area(
        "💼 Paste Job Description",
        height=180,
        placeholder="Paste the complete Job Description here..."
    )

    if not uploaded_file or not job_description.strip():
        st.info("👆 Upload a resume and paste a Job Description to begin.")
        return

    # ==========================================
    # Usage Check
    # ==========================================
    allowed, message = can_use_service(st.session_state.user_email)

    if not allowed:
        st.error(message)
        return

   # ==========================================
# AI Processing Pipeline
# ==========================================

    with st.spinner("Analyzing your resume with AI... This may take a few seconds."):

        resume_text = extract_text_from_pdf(uploaded_file)

        result = analyze_resume(
            resume_text,
            job_description
        )

        gemini_output = generate_ai_content(
            resume_text,
            job_description
        )

    st.subheader("📄 Extracted Resume")

    st.text_area(
        "Resume Content",
        resume_text,
        height=220
    )

    # ==========================================
    # ATS SCORE
    # ==========================================
    st.divider()

    st.markdown("## ⭐ Resume Match Score")
    score = analysis_result.get("ats_score", 0)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Overall ATS Score",
            f"{score}/100"
        )

    with col2:

        if score >= 80:
            st.success("Excellent Match")

        elif score >= 60:
            st.warning("Good Match")

        else:
            st.error("Needs Improvement")

    with col3:
        st.metric(
            "Matched Skills",
            len(result["matched"])
        )

    st.progress(score / 100)

    # ==========================================
    # Tabs
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

        st.markdown(gemini_output)

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

        for i, question in enumerate(
            result["interview_questions"],
            start=1
        ):

            with st.expander(
                f"Question {i}",
                expanded=(i == 1)
            ):
                st.write(question)

    # ==========================================
    # PDF Report
    # ==========================================
    pdf_path = "resume_report.pdf"
    if st.button(
        "📥 Generate AI Report",
        use_container_width=True
    ):
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
                "📥 Download Full AI Report",
                data=pdf_file,
                file_name="AI_Resume_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    # ==========================================
    # Email PDF Report
    # ==========================================
    if st.button(
        "📧 Send Report to My Email",
        use_container_width=True
    ):
        with st.spinner("Sending your report..."):

            email_result = send_email_with_attachment(
                st.session_state.user_email,
                "Your CareerPilot AI Resume Report",
                body,
                pdf_path
            )    

        email_result = send_email_with_attachment(
            st.session_state.user_email,
            "Your CareerPilot AI Resume Report 🚀",
            """
    Hi,

    Your AI Resume Analysis Report has been generated successfully.

    The attached report contains:

    • ATS Resume Score
    • Matched Skills
    • Missing Skills
    • AI Career Suggestions
    • Cover Letter
    • LinkedIn Summary

    Thank you for using CareerPilot AI.

    CareerPilot AI Team
    """,
            pdf_path
        )

        if email_result:
            st.success("✅ Report sent successfully to your email!")
        else:
            st.error("❌ Failed to send email. Please try again.")
    # ==========================================
    # Save Analysis
    # ==========================================
    if st.button(
        "💾 Save Analysis",
        use_container_width=True
    ):

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

        increment_feature_count(
            st.session_state.user_email,
            "resume_analysis_count"
        )
        add_notification(
            st.session_state.user_email,
            "📄 Resume Analysis Completed",
            f"Your resume has been analyzed successfully with an ATS Score of {result['score']}%."
        )

        st.success("✅ Analysis saved successfully!")
