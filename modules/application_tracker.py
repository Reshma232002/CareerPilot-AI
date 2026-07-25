import streamlit as st
import pandas as pd
from backend_db import (
    save_application_status,
    get_application_statuses,
)


def application_tracker():

    st.title("📌 Application Tracker")
    st.caption("Track your application pipeline")

    company = st.text_input("🏢 Company")

    role = st.text_input("💼 Role")

    stage = st.selectbox(

        "Current Stage",

        [

            "Wishlist",

            "Applied",

            "Assessment",

            "Interview",

            "HR Round",

            "Offer",

            "Rejected"

        ]

    )

    notes = st.text_area("Notes")

    if st.button("💾 Save Application"):

        save_application_status(

            st.session_state.user_email,

            company,

            role,

            stage,

            notes

        )

        st.success("Application Saved!")

    st.divider()

    data = get_application_statuses(
        st.session_state.user_email
    )

    if data:

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info("No applications found.")