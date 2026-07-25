import streamlit as st
import smtplib
from email.mime.text import MIMEText

sender = st.secrets["BREVO_EMAIL"]
password = st.secrets["BREVO_PASSWORD"]

receiver = "your_personal_email@gmail.com"   # put your email here

msg = MIMEText("Brevo SMTP test email is working!")
msg["Subject"] = "Brevo Test"
msg["From"] = sender
msg["To"] = receiver

try:
    server = smtplib.SMTP("smtp-relay.brevo.com", 587)
    server.starttls()

    server.login(sender, password)

    server.sendmail(sender, receiver, msg.as_string())

    server.quit()

    st.success("Email sent successfully!")

except Exception as e:
    st.error(e)