import smtplib
import streamlit as st

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email_with_attachment(
    to_email,
    subject,
    body,
    file_path
):
    try:

        smtp_login = st.secrets["BREVO_SMTP_LOGIN"]
        sender_email = st.secrets["BREVO_SENDER_EMAIL"]
        smtp_password = st.secrets["BREVO_PASSWORD"]

        msg = MIMEMultipart()

        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with open(file_path, "rb") as file:
            attachment = MIMEApplication(file.read())

        attachment.add_header(
            "Content-Disposition",
            "attachment",
            filename=file_path.split("/")[-1]
        )

        msg.attach(attachment)

        server = smtplib.SMTP(
            st.secrets["BREVO_SMTP_SERVER"],
            int(st.secrets["BREVO_SMTP_PORT"])
        )

        server.starttls()

        # Login with SMTP credentials
        server.login(
            smtp_login,
            smtp_password
        )

        server.send_message(msg)

        server.quit()

        return True

    except Exception as e:
        print("\n========== EMAIL ERROR ==========")
        print(e)
        print("=================================\n")
        return False
    
def send_welcome_email(to_email):
    try:

        smtp_login = st.secrets["BREVO_SMTP_LOGIN"]
        sender_email = st.secrets["BREVO_SENDER_EMAIL"]
        smtp_password = st.secrets["BREVO_PASSWORD"]

        msg = MIMEMultipart()

        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = "🎉 Welcome to CareerPilot AI"

        body = f"""
Hi,

Welcome to CareerPilot AI! 🚀

Your account has been created successfully.

You can now access:

✅ AI Resume Analyzer
✅ Career Planner
✅ Career DNA
✅ Learning Roadmap
✅ AI Interview Coach
✅ Resume Builder
✅ Job Matcher
✅ AI Copilot

We're excited to help you grow your career.

Happy Learning!

Best Regards,
CareerPilot AI Team
"""

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(
            st.secrets["BREVO_SMTP_SERVER"],
            int(st.secrets["BREVO_SMTP_PORT"])
        )

        server.starttls()

        server.login(
            smtp_login,
            smtp_password
        )

        server.send_message(msg)

        server.quit()

        return True

    except Exception as e:
        print("WELCOME EMAIL ERROR:", e)
        return False   