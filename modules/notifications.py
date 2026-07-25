import streamlit as st

from backend_db import (
    get_notifications,
    mark_notifications_read,
    clear_notifications,
)


def notifications():

    st.title("🔔 Notifications")
    st.caption("Stay updated with your CareerPilot AI activities.")

    notifications = get_notifications(
        st.session_state.user_email
    )

    if not notifications:

        st.info("No notifications available.")

        return

    unread = sum(
        1
        for item in notifications
        if not item.get("read", False)
    )

    st.metric(
        "Unread Notifications",
        unread
    )

    st.divider()

    for item in reversed(notifications):

        if item.get("read", False):

            st.info(
                f"""
### {item['title']}

{item['message']}

🕒 {item['time']}
"""
            )

        else:

            st.success(
                f"""
### {item['title']}

{item['message']}

🕒 {item['time']}
"""
            )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "✅ Mark All Read",
            width="stretch"
        ):

            mark_notifications_read(
                st.session_state.user_email
            )

            st.rerun()

    with col2:

        if st.button(
            "🗑 Clear All",
            width="stretch"
        ):

            clear_notifications(
                st.session_state.user_email
            )

            st.rerun()