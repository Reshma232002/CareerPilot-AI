import streamlit as st
import pandas as pd

from backend_db import get_user_history


def analysis_history():

    st.title("📊 Analysis History")
    st.caption("View all your previous AI Resume Analyses")

    history = get_user_history(st.session_state.user_email)

    if not history:
        st.info("No saved analyses found.")
        return

    # ======================================
    # Search
    # ======================================

    search = st.text_input(
        "🔍 Search by Skill or ATS Score",
        placeholder="Python, AWS, SQL..."
    )

    # ======================================
    # Sort
    # ======================================

    sort_option = st.selectbox(

        "Sort",

        [
            "Newest First",
            "Highest ATS",
            "Lowest ATS"
        ]

    )

    # ======================================
    # Sorting
    # ======================================

    if sort_option == "Highest ATS":
        history = sorted(
            history,
            key=lambda x: x.get("ats_score", 0),
            reverse=True
        )

    elif sort_option == "Lowest ATS":
        history = sorted(
            history,
            key=lambda x: x.get("ats_score", 0)
        )

    else:
        history = list(reversed(history))

    # ======================================
    # Show Analyses
    # ======================================

    for index, item in enumerate(history, start=1):

        matched = ", ".join(item.get("matched_skills", []))

        if (
            search.strip()
            and search.lower() not in matched.lower()
            and search not in str(item.get("ats_score", ""))
        ):
            continue

        score = item.get("ats_score", 0)

        if score >= 80:
            badge = "🟢 Excellent"

        elif score >= 60:
            badge = "🟡 Good"

        else:
            badge = "🔴 Needs Improvement"

        with st.expander(
            f"📄 Analysis {index} | ATS {score}% | {badge}"
        ):

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "ATS Score",
                    f"{score}%"
                )

            with c2:

                st.metric(
                    "Matched Skills",
                    len(item.get("matched_skills", []))
                )

            st.divider()

            st.subheader("✅ Matched Skills")

            for skill in item.get("matched_skills", []):

                st.success(skill)

            st.subheader("❌ Missing Skills")

            for skill in item.get("missing_skills", []):

                st.error(skill)

            st.divider()

            st.subheader("🤖 AI Insights")

            st.markdown(
                item.get(
                    "ai_insights",
                    "No AI Insights"
                )
            )

            st.divider()

            st.subheader("📝 Cover Letter")

            st.text_area(

                "",

                item.get(
                    "cover_letter",
                    ""
                ),

                height=220,

                key=f"cover_{index}"

            )

            st.subheader("💼 LinkedIn Summary")

            st.text_area(

                "",

                item.get(
                    "linkedin_summary",
                    ""
                ),

                height=180,

                key=f"linkedin_{index}"

            )

            st.download_button(

                "📥 Download Cover Letter",

                item.get(
                    "cover_letter",
                    ""
                ),

                file_name=f"cover_letter_{index}.txt",

                use_container_width=True

            )

            st.download_button(

                "📥 Download LinkedIn Summary",

                item.get(
                    "linkedin_summary",
                    ""
                ),

                file_name=f"linkedin_summary_{index}.txt",

                use_container_width=True

            )