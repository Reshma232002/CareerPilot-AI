import streamlit as st
import pandas as pd
from backend_db import save_job_application, get_job_applications


def job_tracker():

    st.title("📋 Job Tracker")
    st.caption("Track all your job applications")

    company = st.text_input("🏢 Company")

    role = st.text_input("💼 Job Role")

    location = st.text_input("📍 Location")

    applied_date = st.date_input("📅 Applied Date")

    status = st.selectbox(

        "Status",

        [

            "Applied",

            "Assessment",

            "Interview",

            "HR Round",

            "Offer",

            "Rejected"

        ]

    )

    notes = st.text_area("Notes")

    if st.button("💾 Save Job"):

        save_job_application(

            st.session_state.user_email,

            company,

            role,

            location,

            str(applied_date),

            status,

            notes

        )

        st.success("Job saved successfully!")

    st.divider()

    jobs = get_job_applications(

        st.session_state.user_email

    )

    if jobs:

        st.dataframe(

            pd.DataFrame(jobs),

            use_container_width=True

        )

    else:

        st.info("No job applications yet.")