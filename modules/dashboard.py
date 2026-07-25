import streamlit as st
import pandas as pd
import plotly.express as px

from backend_db import (
    get_dashboard_stats,
    get_user_history,
    reset_daily_usage_if_needed,
    get_user_doc,
    get_user_profile
)


def dashboard():

    reset_daily_usage_if_needed(st.session_state.user_email)

    stats = get_dashboard_stats(st.session_state.user_email)

    history = get_user_history(st.session_state.user_email)

    user = get_user_doc(st.session_state.user_email)

    profile = get_user_profile(
    st.session_state.user_email
    )

    user_name = profile.get(
        "full_name",
        st.session_state.user_email
    )

    # ==================================================
    # HEADER
    # ==================================================

    st.markdown("""
    # 🚀 CareerPilot AI Dashboard
    ### Your Personal AI Career Assistant

    Welcome back! Here's a snapshot of your career journey today.
    """)

    st.divider()

    # ==================================================
    # WELCOME
    # ==================================================

    st.success(
        f"""
### Good to see you again., {user_name}

Your AI-powered career assistant is ready.

Today's mission:
✔ Improve your ATS Score
✔ Learn a new skill
✔ Apply for your dream job

Let's build your career together! 🚀
"""
    )
    career_goal = profile.get("career_goal", "")

    if career_goal:
        st.info(f"🎯 **Career Goal:** {career_goal}")

    st.divider()

    # ==================================================
    # KPI CARDS
    # ==================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📄 Resume Analyses",
            user.get("resume_analysis_count", 0)
        )

    with col2:
        st.metric(
            "📈 Today's Usage",
            user.get("daily_usage", 0)
        )

    with col3:
        st.metric(
            "👑 Current Plan",
            user.get("plan", "Free").capitalize()
        )

    with col4:

        last_login = user.get("last_login", "N/A")

        st.metric(
            "🕒 Last Login",
            str(last_login)
        )

    st.divider()


    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "⭐ Best ATS",
            f"{stats.get('max_score', 0)}%"
        )

    with c2:
        st.metric(
            "📊 Average ATS",
            f"{stats.get('avg_score', 0)}%"
        )

    with c3:
        st.metric(
            "📄 Total Analyses",
            stats.get("total", 0)
        )

    with c4:
        st.metric(
            "🔥 Today's Usage",
            user.get("daily_usage", 0)
        )

        

    st.divider()
    # ==================================================
    # PROFILE COMPLETION
    # ==================================================

    st.subheader("👤 Profile Completion")

    fields = [
        profile.get("full_name"),
        profile.get("career_goal"),
        profile.get("current_job"),
        profile.get("company"),
        profile.get("education"),
        profile.get("skills"),
        profile.get("linkedin"),
        profile.get("github"),
        profile.get("portfolio"),
        profile.get("location"),
        profile.get("profile_image"),
    ]

    completed = sum(1 for field in fields if field)
    completion = int((completed / len(fields)) * 100)

    st.progress(completion / 100)

    st.write(f"**Profile Completion:** {completion}%")

    if completion == 100:
        st.success("🎉 Awesome! Your profile is complete.")

    elif completion >= 70:
        st.info("👍 Your profile is looking great.")

    else:
        st.warning("Complete your profile to unlock a better experience.")

    st.divider()

    # ==================================================
    # ATS CHART
    # ==================================================

    st.subheader("📈 ATS Progress")

    if history:

        df = pd.DataFrame([

            {
                "Analysis": i + 1,
                "ATS Score": item.get("ats_score",0)

            }

            for i, item in enumerate(history)

        ])

        fig = px.line(

            df,

            x="Analysis",

            y="ATS Score",

            markers=True,

            title="ATS Score Progress"

        )

        fig.update_layout(

            height=420,

            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20
            )

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:

        st.info("No Resume Analysis Available Yet.")

    st.divider()

    # ==================================================
    # RECENT ACTIVITY
    # ==================================================

    st.subheader("🕒 Recent Activity")

    if history:

        latest = history[-5:]

        for item in reversed(latest):

            st.success(
                f"Resume Analysis completed • ATS Score {item.get('ats_score',0)}%"
            )

    else:

        st.info("No activity found.")

    st.divider()

    # ==================================================
    # QUICK ACTIONS
    # ==================================================

    st.subheader("🚀 Quick Actions")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.info("📄 Resume Analyzer")

    with c2:

        st.info("🚀 Career Planner")

    with c3:

        st.info("🤖 AI Copilot")