import streamlit as st
from gemini_engine import generate_ai_content


def career_planner():

    st.title(" AI Career Planner")
    st.caption("Generate a personalized roadmap to reach your dream career.")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        current_role = st.text_input(
            "💼 Current Role",
            placeholder="Desktop Support Engineer"
        )

        experience = st.selectbox(
            "📈 Experience",
            [
                "0-1 Years",
                "1-3 Years",
                "3-5 Years",
                "5+ Years"
            ]
        )

        target_role = st.text_input(
            "🎯 Target Role",
            placeholder="AI Engineer"
        )

    with col2:

        skills = st.text_area(
            "🛠 Current Skills",
            placeholder="Python, Linux, AWS, SQL..."
        )

        timeline = st.selectbox(
            "⏳ Target Timeline",
            [
                "3 Months",
                "6 Months",
                "1 Year",
                "2 Years"
            ]
        )

    st.divider()

    if st.button("🚀 Generate Career Roadmap", use_container_width=True):

        if (
            current_role.strip() == ""
            or target_role.strip() == ""
            or skills.strip() == ""
        ):
            st.warning("Please fill all the fields.")
            return

        prompt = f"""
You are CareerPilot AI.

Create a professional career roadmap.

Current Role:
{current_role}

Experience:
{experience}

Current Skills:
{skills}

Target Role:
{target_role}

Timeline:
{timeline}

Generate the roadmap in Markdown.

Include these sections:

# Career Summary

# Skill Gap Analysis

# Step-by-Step Roadmap

# Certifications

# Projects to Build

# Interview Preparation

# Salary Progression

# Learning Resources

# Weekly Action Plan

# Final Motivation
"""

        with st.spinner("Generating AI Career Roadmap..."):

            roadmap = generate_ai_content(prompt)

        st.success("Roadmap Generated Successfully!")

        st.markdown(roadmap)

        st.download_button(
            "📥 Download Career Roadmap",
            roadmap,
            file_name="Career_Roadmap.md",
            mime="text/markdown"
        )