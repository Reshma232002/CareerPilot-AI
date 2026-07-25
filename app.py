import streamlit as st


# ==================================================
# FIREBASE AUTH
# ==================================================

from firebase_config import auth



# ==================================================
# MODULE IMPORTS
# ==================================================

from modules.dashboard import dashboard
from modules.resume_analyzer import resume_analysis
from modules.analysis_history import analysis_history
from modules.pricing import pricing
from modules.job_matcher import job_matcher
from modules.interview_coach import interview_coach
from modules.career_planner import career_planner
from modules.ai_copilot import ai_copilot
from modules.settings import settings
from modules.career_dna import career_dna
from modules.learning_roadmap import learning_roadmap
from modules.skill_gap import skill_gap
from modules.resume_builder import resume_builder
from modules.admin_dashboard import admin_dashboard
from modules.recruiter_dashboard import recruiter_dashboard
from modules.job_tracker import job_tracker
from modules.application_tracker import application_tracker
from modules.profile import profile
from modules.notifications import notifications



# ==================================================
# SERVICES
# ==================================================

from email_utils import send_welcome_email


from backend_db import (
    create_user_if_not_exists,
    update_last_login,
    get_user_profile,
    add_notification,
    get_unread_notification_count
)



# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(

    page_title="CareerPilot AI",

    page_icon="assets/logos/favicon.png",

    layout="wide",

    initial_sidebar_state="expanded"

)



# ==================================================
# LOAD CSS
# ==================================================

try:

    with open(
        "assets/styles.css",
        "r",
        encoding="utf-8"
    ) as file:


        st.markdown(

            f"""
            <style>
            {file.read()}
            </style>
            """,

            unsafe_allow_html=True

        )


except Exception:

    pass




# ==================================================
# SESSION STATE
# ==================================================

if "user" not in st.session_state:

    st.session_state.user = None


if "user_email" not in st.session_state:

    st.session_state.user_email = ""


if "premium_order" not in st.session_state:

    st.session_state.premium_order = None


if "recruiter_order" not in st.session_state:

    st.session_state.recruiter_order = None




# ==================================================
# LOGOUT
# ==================================================

def logout():

    st.session_state.user = None

    st.session_state.user_email = ""

    st.session_state.premium_order = None

    st.session_state.recruiter_order = None


    st.rerun()





# ==================================================
# AUTHENTICATION
# ==================================================

def login_signup():


    auth_mode = st.radio(

        "Account",

        [
            "Login",
            "Create Account"
        ],

        horizontal=True

    )


    email = st.text_input(

        "Email Address",

        placeholder="Enter your email"

    )


    password = st.text_input(

        "Password",

        type="password",

        placeholder="Enter your password"

    )



    st.write("")



    if auth_mode == "Create Account":


        if st.button(

            "Create Account",

            use_container_width=True

        ):


            try:


                with st.spinner(

                    "Creating account..."

                ):


                    user = auth.create_user_with_email_and_password(

                        email,

                        password

                    )


                    auth.send_email_verification(

                        user["idToken"]

                    )


                    create_user_if_not_exists(

                        email

                    )


                    add_notification(

                        email,

                        "Welcome to CareerPilot AI",

                        "Your account has been created successfully."

                    )


                    email_sent = send_welcome_email(

                        email

                    )



                if email_sent:


                    st.success(

                        "Account created successfully."

                    )


                else:


                    st.warning(

                        "Account created but email could not be sent."

                    )



            except Exception as e:


                st.error(e)





    else:


        if st.button(

            "Sign In",

            use_container_width=True

        ):


            try:


                with st.spinner(

                    "Signing in..."

                ):


                    user = auth.sign_in_with_email_and_password(

                        email,

                        password

                    )


                    st.session_state.user = user


                    st.session_state.user_email = email


                    update_last_login(

                        email

                    )


                st.rerun()



            except Exception:


                st.error(

                    "Invalid email or password."

                )

def render_login_page():

    left, right = st.columns(
        [1.1,0.9],
        gap="large"
    )


    # ==========================
    # LEFT SIDE
    # ==========================

    with left:


        logo_col, name_col = st.columns(
            [0.25,0.75],
            gap="small"
        )


        with logo_col:

            st.image(
                "assets/logos/logo.png",
                width=120
            )


        with name_col:

            st.image(
                "assets/logos/wordmark.png",
                width=320
            )



        st.markdown(
            """
            <h1>
            AI-Powered Career Intelligence Platform
            </h1>

            <p>
            Build better resumes, improve ATS scores,
            prepare for interviews, and accelerate your
            career growth with artificial intelligence.
            </p>
            """,
            unsafe_allow_html=True
        )


        c1,c2 = st.columns(2)


        with c1:

            st.info(
            """
            **Resume Intelligence**

            AI-powered resume analysis and optimization.
            """
            )

            st.info(
            """
            **Career Growth**

            Personalized career planning and roadmap.
            """
            )


        with c2:

            st.info(
            """
            **ATS Optimization**

            Improve resume ranking for recruiters.
            """
            )


            st.info(
            """
            **AI Copilot**

            Your personal career assistant.
            """
            )




    # ==========================
    # RIGHT SIDE
    # ==========================


    with right:

        st.markdown(
                """
                <div class="login-card-wrapper">
                """,
                unsafe_allow_html=True
        )



        with st.container(border=True):


            st.markdown(
            """
            <h2 style="text-align:center">
            Welcome Back
            </h2>

            <p style="text-align:center">
            Sign in to continue your career journey.
            </p>
            """,
            unsafe_allow_html=True
            )


            login_signup()



    st.markdown(
    """
    <div class="footer">
    CareerPilot AI v1.0
    <br>
    © 2026 CareerPilot AI
    </div>
    """,
    unsafe_allow_html=True
    )
# ==================================================
# MAIN APPLICATION
# ==================================================

if st.session_state.user:



    # ==================================================
    # SIDEBAR
    # ==================================================

    with st.sidebar:



        st.image(

            "assets/logos/logo.png",

            width=80

        )


        st.image(

            "assets/logos/wordmark.png",

            width=180

        )



        st.caption(

            "AI Resume Intelligence Platform"

        )



        st.divider()



        # ----------------------------------------------
        # USER PROFILE
        # ----------------------------------------------


        user_profile = get_user_profile(

            st.session_state.user_email

        )



        profile_image = user_profile.get(

            "profile_image",

            ""

        )



        full_name = user_profile.get(

            "full_name",

            "User"

        )



        if profile_image:


            try:


                st.image(

                    profile_image,

                    width=90

                )


            except Exception:


                pass




        st.markdown(

            f"""

            ### {full_name}


            <small>

            {st.session_state.user_email}

            </small>

            """,

            unsafe_allow_html=True

        )



        unread_count = get_unread_notification_count(

            st.session_state.user_email

        )



        if unread_count > 0:


            notification_label = (

                f"Notifications ({unread_count})"

            )


        else:


            notification_label = "Notifications"





        st.divider()



        # ----------------------------------------------
        # NAVIGATION
        # ----------------------------------------------


        page = st.radio(

            "Navigation",

            [

                "Dashboard",

                notification_label,

                "My Profile",

                "Resume Review",

                "Career Planner",

                "Career Assessment",

                "Learning Roadmap",

                "Job Matcher",

                "Interview Coach",

                "Skill Gap Analyzer",

                "Resume Builder",

                "Admin Console",

                "Recruiter Portal",

                "Job Applications",

                "Application Tracker",

                "Reports",

                "AI Copilot",

                "Pricing",

                "Settings"

            ]

        )          

                # ==================================================
        # LOGOUT BUTTON
        # ==================================================

        st.divider()


        if st.button(

            "Logout",

            use_container_width=True

        ):

            logout()



    # ==================================================
    # PAGE ROUTING
    # ==================================================

    if page == "Dashboard":

        dashboard()



    elif page.startswith("Notifications"):

        notifications()



    elif page == "My Profile":

        profile()



    elif page == "Resume Review":

        resume_analysis()



    elif page == "Career Planner":

        career_planner()



    elif page == "Career Assessment":

        career_dna()



    elif page == "Learning Roadmap":

        learning_roadmap()



    elif page == "Job Matcher":

        job_matcher()



    elif page == "Interview Coach":

        interview_coach()



    elif page == "Skill Gap Analyzer":

        skill_gap()



    elif page == "Resume Builder":

        resume_builder()



    elif page == "Admin Console":

        admin_dashboard()



    elif page == "Recruiter Portal":

        recruiter_dashboard()



    elif page == "Job Applications":

        job_tracker()



    elif page == "Application Tracker":

        application_tracker()



    elif page == "Reports":

        analysis_history()



    elif page == "AI Copilot":

        ai_copilot()



    elif page == "Pricing":

        pricing()



    elif page == "Settings":

        settings()




# ==================================================
# NOT LOGGED IN
# ==================================================

else:


    render_login_page()      
