import streamlit as st
from gemini_engine import generate_ai_content


def learning_roadmap():

    st.title("📚 AI Learning Roadmap")
    st.caption("Generate a personalized learning plan.")

    target_role = st.text_input(
        "Target Role",
        placeholder="AI Engineer"
    )

    current_skills = st.text_area(
        "Current Skills",
        placeholder="Python, SQL, Linux..."
    )

    duration = st.selectbox(
        "Learning Duration",
        [
            "1 Month",
            "3 Months",
            "6 Months",
            "12 Months"
        ]
    )

    if st.button(
        "🚀 Generate Roadmap",
        use_container_width=True
    ):

        if target_role.strip() == "" or current_skills.strip() == "":
            st.warning("Please complete all fields.")
            return

        prompt = f"""
You are an expert career mentor.

Create a detailed learning roadmap.

Target Role:
{target_role}

Current Skills:
{current_skills}

Duration:
{duration}

Include:

# Overview

# Weekly Learning Plan

# Skills to Learn

# Best Certifications

# Recommended Projects

# Free Resources

# Interview Preparation

# Final Checklist

Return in Markdown.
"""

        with st.spinner("Generating Roadmap..."):
            roadmap = generate_ai_content(prompt)

        st.success("Roadmap Generated!")

        st.markdown(roadmap)

        st.download_button(
            "📥 Download Roadmap",
            roadmap,
            file_name="Learning_Roadmap.md",
            mime="text/markdown"
        )