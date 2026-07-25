import streamlit as st
import pandas as pd
import tempfile

from backend_db import get_all_resume_analyses
from pdf_generator import generate_pdf

def recruiter_dashboard():

    st.title("👔 Recruiter Dashboard")
    st.caption("Discover top candidates using CareerPilot AI")

    data = get_all_resume_analyses()

    if not data:
        st.info("No candidates available.")
        return

    df = pd.DataFrame(data)

    # ==========================================
    # Recruiter Statistics
    # ==========================================

    total_candidates = len(df)

    average_ats = round(df["ats_score"].mean(), 2)

    above_80 = len(df[df["ats_score"] >= 80])

    below_50 = len(df[df["ats_score"] < 50])

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "👥 Candidates",
            total_candidates
        )

    with c2:
        st.metric(
            "⭐ Average ATS",
            f"{average_ats}%"
        )

    with c3:
        st.metric(
            "🟢 ATS ≥ 80%",
            above_80
        )

    with c4:
        st.metric(
            "🔴 ATS < 50%",
            below_50
        )

    st.divider()

    # ==========================================
    # Search & Filters
    # ==========================================

    left, right = st.columns(2)

    with left:

        search = st.text_input(
            "🔍 Search Skills",
            placeholder="Python, AWS, SQL..."
        )

    with right:

        min_score = st.slider(
            "Minimum ATS Score",
            0,
            100,
            60
        )

    if search:

        df = df[
            df["matched_skills"]
            .astype(str)
            .str.contains(search, case=False)
        ]

    df = df[df["ats_score"] >= min_score]

    st.divider()

    # ==========================================
    # Candidate List
    # ==========================================

    st.subheader("📄 Candidate Profiles")

    display_df = df[
        [
            "user_email",
            "ats_score",
            "matched_skills",
            "missing_skills"
        ]
    ]

    display_df.columns = [
        "Email",
        "ATS Score",
        "Matched Skills",
        "Missing Skills"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.success(f"Showing {len(display_df)} candidate(s)")

    st.divider()

    st.subheader("👤 Candidate Details")

    candidate_list = df["user_email"].tolist()

    selected_candidate = st.selectbox(
        "Select Candidate",
        candidate_list
    )

    if selected_candidate:

        candidate = df[
            df["user_email"] == selected_candidate
        ].iloc[0]

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 📧 Candidate Information")

            st.write(f"**Email:** {candidate['user_email']}")
            st.write(f"**ATS Score:** {candidate['ats_score']}%")

        with col2:

            st.markdown("### 📊 Skills")

            st.write("**✅ Matched Skills**")
            st.write(candidate["matched_skills"])

            st.write("**❌ Missing Skills**")
            st.write(candidate["missing_skills"])

        st.divider()

        st.markdown("### 🤖 AI Insights")
        st.info(candidate.get("ai_insights", "No AI insights available."))

        st.markdown("### 💌 AI Cover Letter")
        st.text_area(
            "",
            candidate.get("cover_letter", ""),
            height=180,
            disabled=True
        )

        st.markdown("### 🔗 LinkedIn Summary")
        st.text_area(
            "",
            candidate.get("linkedin_summary", ""),
            height=150,
            disabled=True
        )

        st.markdown("### 📄 Resume Text")
        st.text_area(
            "",
            candidate.get("resume_text", ""),
            height=300,
            disabled=True
        )

        st.divider()

    if st.button("📄 Generate Candidate Report"):

        pdf_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        )

        generate_pdf(
            filename=pdf_file.name,
            candidate_email=candidate["user_email"],
            ats_score=candidate["ats_score"],
            matched_skills=candidate["matched_skills"],
            missing_skills=candidate["missing_skills"],
            cover_letter=candidate.get("cover_letter", ""),
            linkedin_summary=candidate.get("linkedin_summary", ""),
            ai_insights=candidate.get("ai_insights", "")
        )

        pdf_file.close()

        with open(pdf_file.name, "rb") as f:

            st.download_button(
                label="⬇ Download Candidate Report",
                data=f.read(),
                file_name="Candidate_Report.pdf",
                mime="application/pdf"
            )