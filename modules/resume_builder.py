import streamlit as st
from gemini_engine import generate_ai_content


def resume_builder():

    st.title("📄 AI Resume Builder")
    st.caption("Generate a professional ATS-friendly resume.")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")

    target_role = st.text_input(
        "Target Role",
        placeholder="Python Developer"
    )

    skills = st.text_area(
        "Skills",
        placeholder="Python, SQL, AWS..."
    )

    education = st.text_area(
        "Education"
    )

    experience = st.text_area(
        "Experience"
    )

    projects = st.text_area(
        "Projects"
    )

    if st.button(
        "🚀 Generate Resume",
        use_container_width=True
    ):

        if (
            name.strip() == "" or
            target_role.strip() == ""
        ):
            st.warning("Please fill required fields.")
            return

        prompt = f"""
Create a professional ATS Resume.

Name:
{name}

Email:
{email}

Phone:
{phone}

Target Role:
{target_role}

Skills:
{skills}

Education:
{education}

Experience:
{experience}

Projects:
{projects}

Generate in Markdown.

Include:

Professional Summary

Skills

Experience

Projects

Education

Certifications

Achievements
"""

        with st.spinner("Generating Resume..."):

            resume = generate_ai_content(prompt)

        st.success("Resume Generated!")

        st.markdown(resume)

        st.download_button(
            "📥 Download Resume",
            resume,
            file_name="ATS_Resume.md",
            mime="text/markdown"
        )