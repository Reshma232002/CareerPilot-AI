import streamlit as st
from gemini_engine import generate_ai_content


def skill_gap():

    st.title("📊 AI Skill Gap Analyzer")
    st.caption("Find the gap between your current skills and your dream job.")

    target_role = st.text_input(
        "🎯 Target Role",
        placeholder="AI Engineer"
    )

    current_skills = st.text_area(
        "🛠 Current Skills",
        placeholder="Python, SQL, Linux..."
    )

    experience = st.selectbox(
        "Experience",
        [
            "Student",
            "Fresher",
            "1-3 Years",
            "3-5 Years",
            "5+ Years"
        ]
    )

    if st.button(
        "🚀 Analyze Skill Gap",
        use_container_width=True
    ):

        if target_role.strip() == "" or current_skills.strip() == "":
            st.warning("Please complete all fields.")
            return

        prompt = f"""
You are an expert Career Coach.

Analyze this user's skill gap.

Target Role:
{target_role}

Experience:
{experience}

Current Skills:
{current_skills}

Generate a detailed report.

Include:

# Current Strengths

# Missing Skills

# Skill Priority (High / Medium / Low)

# Recommended Technologies

# Certifications

# Projects

# Estimated Learning Time

# Interview Readiness

# Final Recommendation

Return in Markdown.
"""

        with st.spinner("Analyzing Skill Gap..."):
            result = generate_ai_content(prompt)

        st.success("Skill Gap Analysis Completed!")

        st.markdown(result)

        st.download_button(
            "📥 Download Skill Gap Report",
            result,
            file_name="Skill_Gap_Report.md",
            mime="text/markdown"
        )