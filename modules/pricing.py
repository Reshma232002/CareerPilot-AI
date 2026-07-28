import streamlit as st
import streamlit.components.v1 as components

from payment import (
    create_order,
    verify_payment,
    get_user_plan,
)


def razorpay_checkout(order, plan_name):

    checkout_html = f"""
    <script src="https://checkout.razorpay.com/v1/checkout.js"></script>

    <script>

    var options = {{

        "key": "{order['key']}",

        "amount": "{order['amount']}",

        "currency": "INR",

        "name": "CareerPilot AI",

        "description": "{plan_name} Subscription",

        "order_id": "{order['id']}",

        "handler": function(response) {{

            window.parent.postMessage({{
                payment_id: response.razorpay_payment_id,
                order_id: response.razorpay_order_id,
                signature: response.razorpay_signature
            }}, "*");

        }}

    }};


    var rzp = new Razorpay(options);

    rzp.open();

    </script>
    """

    components.html(
        checkout_html,
        height=600
    )



def pricing():

    st.title("Pricing Plans")
    st.caption("Upgrade your CareerPilot AI experience.")


    # -----------------------------
    # Current Plan
    # -----------------------------
    current_plan = get_user_plan(
        st.session_state.user_email
    )

    st.success(
        f"Current Plan: **{current_plan.upper()}**"
    )


    st.divider()


    col1, col2, col3 = st.columns(3)



    # =====================================================
    # FREE PLAN
    # =====================================================
    with col1:

        st.subheader("🆓 Free")

        st.markdown("""
### $0 / month

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

            st.success(
                "You're already on Premium 🎉"
            )

        else:

            if st.button(
                "Upgrade to Premium ₹99",
                use_container_width=True
            ):

                order = create_order(
                    "premium",
                    st.session_state.user_email
                )


                st.session_state.premium_order = order["id"]


                razorpay_checkout(
                    order,
                    "Premium Plan"
                )



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

            st.success(
                "You're already on Recruiter 🎉"
            )


        else:

            if st.button(
                "Upgrade to Recruiter ₹299",
                use_container_width=True
            ):

                order = create_order(
                    "recruiter",
                    st.session_state.user_email
                )


                st.session_state.recruiter_order = order["id"]


                razorpay_checkout(
                    order,
                    "Recruiter Plan"
                )
