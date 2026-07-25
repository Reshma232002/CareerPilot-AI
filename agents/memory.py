import streamlit as st


def add_message(role, content):

    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.session_state.messages.append({
        "role": role,
        "content": content
    })


def get_history():

    if "messages" not in st.session_state:
        return []

    return st.session_state.messages


def clear_history():
    st.session_state.messages = []