import streamlit as st
from gemini_engine import generate_ai_content


def career_dna():

    st.title("🧬 AI Career DNA")
    st.caption("Discover your career personality and ideal career path.")

    name = st.text_input("Your Name")

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

    interests = st.text_area(
        "Your Interests",
        placeholder="AI, Coding, Leadership, Design..."
    )

    strengths = st.text_area(
        "Your Strengths",
        placeholder="Problem Solving, Communication..."
    )

    goals = st.text_area(
        "Career Goals",
        placeholder="Become an AI Engineer..."
    )

    if st.button(
        "🧬 Generate Career DNA",
        use_container_width=True
    ):

        if (
            name.strip() == "" or
            interests.strip() == "" or
            strengths.strip() == "" or
            goals.strip() == ""
        ):
            st.warning("Please fill all the fields.")
            st.stop()

        prompt = f"""
You are an expert Career Coach.

Analyze this person's career profile.

Name:
{name}

Experience:
{experience}

Interests:
{interests}

Strengths:
{strengths}

Career Goals:
{goals}

Generate a professional report.

Include:

# Career Personality

# Top Strengths

# Weaknesses

# Ideal Careers

# Leadership Score (/10)

# Communication Score (/10)

# Technical Score (/10)

# Learning Style

# Career Advice

# Next 12 Months Plan

Return in Markdown.
"""

        with st.spinner("Analyzing Career DNA..."):

            result = generate_ai_content(prompt)

        st.success("Career DNA Generated!")

        st.markdown(result)

        st.download_button(
            "📥 Download Career DNA",
            result,
            file_name="Career_DNA.md",
            mime="text/markdown"
        )