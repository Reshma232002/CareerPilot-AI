import streamlit as st

from agents.router import execute
from agents.memory import (
    add_message,
    get_history,
    clear_history,
)


def ai_copilot():

    st.title(" CareerPilot AI Copilot")
    st.caption("Your personal AI Career Assistant")

    col1, col2 = st.columns([8, 2])

    with col2:
        if st.button("🗑 Clear Chat", use_container_width=True):
            clear_history()
            st.rerun()

    st.write("Ask anything about your career.")

    history = get_history()

    # Show previous messages
    for msg in history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    prompt = st.chat_input("Ask CareerPilot AI...")

    if prompt:

        add_message("user", prompt)

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):

            response = execute(
                prompt,
                history=get_history()
            )

        add_message("assistant", response)

        with st.chat_message("assistant"):
            st.markdown(response)