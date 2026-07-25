import os
import shutil
import streamlit as st

from backend_db import (
    save_user_profile,
    get_user_profile
)


# ==================================================
# PROFILE PAGE
# ==================================================
def profile():

    st.title("👤 My Profile")
    st.caption("Manage your CareerPilot AI profile.")

    # ----------------------------------------------
    # Load Existing Profile
    # ----------------------------------------------
    data = get_user_profile(st.session_state.user_email)

    profile_image = data.get("profile_image", "")

    # ----------------------------------------------
    # Personal Information
    # ----------------------------------------------
    st.subheader("👤 Personal Information")

    full_name = st.text_input(
        "Full Name",
        value=data.get("full_name", "")
    )

    career_goal = st.text_input(
        "Career Goal",
        value=data.get("career_goal", "")
    )

    current_job = st.text_input(
        "Current Job Title",
        value=data.get("current_job", "")
    )

    company = st.text_input(
        "Company",
        value=data.get("company", "")
    )

    education = st.text_input(
        "Education",
        value=data.get("education", "")
    )

    skills = st.text_area(
        "Skills",
        value=data.get("skills", ""),
        height=120
    )

    # ----------------------------------------------
    # Social Links
    # ----------------------------------------------
    st.subheader("🌐 Social Profiles")

    linkedin = st.text_input(
        "LinkedIn URL",
        value=data.get("linkedin", "")
    )

    github = st.text_input(
        "GitHub URL",
        value=data.get("github", "")
    )

    portfolio = st.text_input(
        "Portfolio URL",
        value=data.get("portfolio", "")
    )

    location = st.text_input(
        "Location",
        value=data.get("location", "")
    )

    st.divider()

    # ----------------------------------------------
    # Profile Picture
    # ----------------------------------------------
    st.subheader("📷 Profile Picture")

    # Show current profile picture
    if profile_image and os.path.exists(profile_image):
        st.image(
            profile_image,
            width=180,
            caption="Current Profile Picture"
        )

    uploaded_image = st.file_uploader(
        "Upload Profile Picture",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_image is not None:

        image_name = (
            st.session_state.user_email
            .replace("@", "_")
            .replace(".", "_")
            + ".png"
        )

        image_path = os.path.join(
            "assets/profile_images",
            image_name
        )

        with open(image_path, "wb") as f:
            shutil.copyfileobj(uploaded_image, f)

        profile_image = image_path

        st.success("✅ Profile picture uploaded successfully!")

        st.image(
            profile_image,
            width=180
        )

    st.divider()

    # ----------------------------------------------
    # Save Profile
    # ----------------------------------------------
    if st.button(
        "💾 Save Profile",
        use_container_width=True
    ):

        profile_data = {
            "full_name": full_name,
            "career_goal": career_goal,
            "current_job": current_job,
            "company": company,
            "education": education,
            "skills": skills,
            "linkedin": linkedin,
            "github": github,
            "portfolio": portfolio,
            "location": location,
            "profile_image": profile_image,
        }

        save_user_profile(
            st.session_state.user_email,
            profile_data
        )

        st.success("✅ Profile saved successfully!")

        st.balloons()