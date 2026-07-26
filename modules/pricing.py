import streamlit as st
import streamlit.components.v1 as components

from payment import (
    create_order,
    verify_payment,
    get_user_plan,
)


def pricing():

    st.title(" Pricing Plans")
    st.caption("Upgrade your CareerPilot AI experience.")

    # -----------------------------
    # Current Plan
    # -----------------------------
    current_plan = get_user_plan(st.session_state.user_email)

    st.success(f"Current Plan: **{current_plan.upper()}**")

    st.divider()

    # -----------------------------
    # Session State
    # -----------------------------
    if "premium_order" not in st.session_state:
        st.session_state.premium_order = None

    if "recruiter_order" not in st.session_state:
        st.session_state.recruiter_order = None

    col1, col2, col3 = st.columns(3)

    # =====================================================
    # FREE PLAN
    # =====================================================
    with col1:

        st.subheader("🆓 Free")

        st.markdown("""
### ₹0 / month

✅ 1 Resume Analysis / Day

✅ AI Resume Score

✅ Basic AI Insights

❌ AI Copilot Unlimited

❌ Premium Reports

❌ Priority Support
""")

    # =====================================================
    # PREMIUM PLAN
    # =====================================================
    with col2:

        st.subheader("⭐ Premium")

        st.markdown("""
### ₹99 / month

✅ Unlimited Resume Analysis

✅ Unlimited AI Copilot

✅ AI Cover Letter

✅ LinkedIn Optimizer

✅ Interview Questions

✅ PDF Reports

✅ Priority Support
""")

        if current_plan.lower() == "premium":

            st.success("You're already on Premium 🎉")

        else:

            if st.button("Upgrade to Premium ₹99", use_container_width=True):

                order = create_order(99)

                st.session_state.premium_order = order["id"]

                checkout_html = f"""
                <script src="https://checkout.razorpay.com/v1/checkout.js"></script>

                <script>
                var options = {{
                    "key": "{st.secrets["RAZORPAY_KEY_ID"]}",
                    "amount": "9900",
                    "currency": "INR",
                    "name": "CareerPilot AI",
                    "description": "Premium Plan",
                    "order_id": "{order['id']}",
                    "handler": function (response){{
                        window.parent.postMessage(response, "*");
                    }}
                }};

                var rzp = new Razorpay(options);
                rzp.open();
                </script>
                """

                components.html(checkout_html, height=600)

        if st.session_state.premium_order:

            st.markdown("### Verify Payment")

            order_id = st.text_input("Order ID")

            payment_id = st.text_input("Payment ID")

            signature = st.text_input("Signature")

            if st.button("Verify Premium Payment"):

                if verify_payment(
                    order_id,
                    payment_id,
                    signature,
                    st.session_state.user_email        
                ):

                    st.success("🎉 Premium Activated!")

                    st.session_state.premium_order = None

                    st.rerun()

                else:

                    st.error("Payment Verification Failed")

    # =====================================================
    # RECRUITER PLAN
    # =====================================================
    with col3:

        st.subheader("🚀 Recruiter")

        st.markdown("""
### ₹299 / month

Everything in Premium +

✅ Recruiter Dashboard

✅ Bulk Resume Screening

✅ AI Candidate Ranking

✅ Hiring Analytics

✅ Candidate Reports

✅ Team Access

✅ Priority Support
""")

        if current_plan.lower() == "recruiter":

            st.success("You're already on Recruiter 🎉")

        else:

            if st.button("Upgrade to Recruiter ₹299", use_container_width=True):

                order = create_order(299)

                st.session_state.recruiter_order = order["id"]

                checkout_html = f"""
                <script src="https://checkout.razorpay.com/v1/checkout.js"></script>

                <script>
                var options = {{
                    "key": "{st.secrets["RAZORPAY_KEY_ID"]}",
                    "amount": "29900",
                    "currency": "INR",
                    "name": "CareerPilot AI",
                    "description": "Recruiter Plan",
                    "order_id": "{order['id']}",
                    "handler": function(response){{
                        window.parent.postMessage(response, "*");
                    }}
                }};

                var rzp = new Razorpay(options);
                rzp.open();
                </script>
                """

                components.html(checkout_html, height=600)

        if st.session_state.recruiter_order:

            st.markdown("### Verify Payment")

            order_id = st.text_input("Recruiter Order ID")

            payment_id = st.text_input("Recruiter Payment ID")

            signature = st.text_input("Recruiter Signature")

            if st.button("Verify Recruiter Payment"):

                if verify_payment(
                    order_id,
                    payment_id,
                    signature,
                    st.session_state.user_email
                ):

                    st.success("🎉 Recruiter Activated!")

                    st.session_state.recruiter_order = None

                    st.rerun()

                else:

                    st.error("Payment Verification Failed")
