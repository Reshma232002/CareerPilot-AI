import streamlit as st
import plotly.express as px
import pandas as pd

from backend_db import (
    get_admin_dashboard_stats,
    get_all_resume_analyses
)


def admin_dashboard():

    st.title("🛠 Admin Analytics")
    st.caption("CareerPilot AI Platform Overview")

    stats = get_admin_dashboard_stats()

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.metric(
            "👥 Users",
            stats["total_users"]
        )

    with c2:
        st.metric(
            "💎 Premium",
            stats["premium_users"]
        )

    with c3:
        st.metric(
            "👔 Recruiters",
            stats["recruiter_users"]
        )

    with c4:
        st.metric(
            "📄 Resume Analyses",
            stats["total_resume_analyses"]
        )

    with c5:
        st.metric(
            "⚡ Total Usage",
            stats["total_usage"]
        )

    st.divider()

    analyses = get_all_resume_analyses()

    if not analyses:
        st.info("No analytics available yet.")
        return

    df = pd.DataFrame(analyses)

    st.subheader("📊 ATS Score Distribution")

    fig = px.histogram(
        df,
        x="ats_score",
        nbins=10,
        title="Candidate ATS Scores"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    st.subheader("🏆 Top Candidates")

    top = df.sort_values(
        by="ats_score",
        ascending=False
    )

    st.dataframe(
        top[
            [
                "user_email",
                "ats_score",
                "matched_skills"
            ]
        ].head(10),
        use_container_width=True,
        hide_index=True
    )