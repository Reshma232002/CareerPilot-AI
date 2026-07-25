import streamlit as st
from backend_db import get_user_doc


def settings():

    st.title("⚙️ Settings")

    if "user_email" not in st.session_state:
        st.warning("Please login first.")
        return

    user = get_user_doc(st.session_state.user_email)

    st.subheader("👤 Account Information")

    col1, col2 = st.columns(2)

    with col1:
        st.text_input(
            "Email",
            value=st.session_state.user_email,
            disabled=True
        )

    with col2:
        st.text_input(
            "Current Plan",
            value=user.get("plan", "Free").capitalize(),
            disabled=True
        )

    st.divider()

    st.subheader("📊 Usage")

    st.metric(
        "Today's Analyses",
        user.get("daily_usage", 0)
    )

    st.divider()

    st.subheader("🚀 Upcoming Features")

    st.checkbox(
        "Email Notifications",
        disabled=True
    )

    st.checkbox(
        "Dark Mode",
        disabled=True
    )

    st.checkbox(
        "Weekly Career Report",
        disabled=True
    )

    st.checkbox(
        "Interview Reminder",
        disabled=True
    )

    st.info("These features will be available soon.")