import streamlit as st
from gemini_engine import generate_ai_content


def interview_coach():

    st.title("🎤 AI Interview Coach")
    st.caption("Practice technical and HR interviews with AI.")

    role = st.text_input(
        "Target Role",
        placeholder="Python Developer"
    )

    experience = st.selectbox(
        "Experience",
        [
            "Fresher",
            "1-3 Years",
            "3-5 Years",
            "5+ Years"
        ]
    )

    interview_type = st.selectbox(
        "Interview Type",
        [
            "HR Interview",
            "Technical Interview",
            "Managerial Interview",
            "Mixed Interview"
        ]
    )

    if st.button(
        "🚀 Generate Interview Questions",
        use_container_width=True
    ):

        if role.strip() == "":
            st.warning("Please enter a target role.")
            return

        prompt = f"""
You are an experienced interviewer.

Generate 15 interview questions.

Role:
{role}

Experience:
{experience}

Interview Type:
{interview_type}

For every question include:

1. Question
2. Why interviewer asks it
3. Sample Answer
4. Common Mistakes
5. Difficulty (Easy/Medium/Hard)

Return in Markdown.
"""

        try:

            with st.spinner("Generating Interview Questions..."):
                result = generate_ai_content(prompt)

            st.success("Interview Questions Generated!")

            st.markdown(result)

            st.download_button(
                "📥 Download Interview Questions",
                data=result,
                file_name="Interview_Questions.md",
                mime="text/markdown"
            )

        except Exception as e:
            st.error(f"Error:\n\n{e}")