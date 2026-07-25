import google.generativeai as genai
import streamlit as st

# Configure Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Gemini Model
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_ai_content(prompt, job_description=None):
    """
    If only 'prompt' is passed:
        - Used by AI Copilot, Career Planner, etc.

    If 'prompt' and 'job_description' are passed:
        - Used by Resume Analyzer.
    """

    try:

        # Resume Analyzer
        if job_description is not None:

            final_prompt = f"""
You are an expert ATS Resume Reviewer.

Analyze the following resume against the job description.

Resume:
{prompt}

Job Description:
{job_description}

Provide:

# Overall Analysis

# Strengths

# Weaknesses

# Missing Skills

# Resume Improvement Suggestions

# ATS Optimization Tips

# Final Recommendation
"""

        else:
            # AI Copilot / Career Planner / Others
            final_prompt = prompt

        response = model.generate_content(final_prompt)

        if response.parts:
            return response.text

        return "No response generated."

    except Exception as e:
        return f"Gemini Exception:\n{e}"