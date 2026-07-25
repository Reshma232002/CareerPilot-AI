import streamlit as st
from pdf_utils import extract_text_from_pdf
from gemini_engine import generate_ai_content

def job_matcher():

    st.title("🎯 AI Job Matcher")
    st.caption("Find the best matching jobs based on your resume.")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"]
    )

    if uploaded_file is None:
        return

    resume = extract_text_from_pdf(uploaded_file)

    if st.button("🔍 Find Matching Jobs", use_container_width=True):

        prompt = f"""
You are an AI Career Coach.

Based on this resume,

Recommend the TOP 10 job roles.

For each role provide:

- Job Title
- Match Percentage
- Why it matches
- Skills to improve
- Expected Salary (India)
- Difficulty (Easy/Medium/Hard)

Resume:

{resume}

Return in Markdown.
"""

        with st.spinner("Finding best jobs..."):

            result = generate_ai_content(prompt)

        st.markdown(result)

        st.download_button(
            "📥 Download Report",
            result,
            file_name="job_match_report.md",
            mime="text/markdown"
        )