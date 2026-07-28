import streamlit as st
import razorpay
import hmac
import hashlib
from datetime import datetime
from firebase_admin import firestore
from backend_db import db


client = razorpay.Client(
    auth=(
        st.secrets["RAZORPAY_KEY_ID"],
        st.secrets["RAZORPAY_KEY_SECRET"]
    )
)




def save_order(email, order_id, plan, amount):

    try:
        user_id = email.replace(".", "_")

        db.collection("payments").document(order_id).set({

            "email": email,
            "user_id": user_id,
            "order_id": order_id,
            "plan": plan,
            "amount": amount,
            "status": "created",
            "created_at": datetime.now()

        })

        print("Order saved successfully")

    except Exception as e:
        print("Order save failed:", e)

def create_order(plan, email):

    if plan == "premium":
        amount = 99

    elif plan == "recruiter":
        amount = 299

    else:
        amount = 0


    order = client.order.create(
        {
            "amount": amount * 100,
            "currency": "INR",
            "payment_capture": 1,
            "notes": {
                "plan": plan,
                "email": email
            }
        }
    )

    print("RAZORPAY RESPONSE:", order)
    save_order(
        email,
        order["id"],
        plan,
        amount
    )

    order["key"] = st.secrets["RAZORPAY_KEY_ID"]

    return order



def verify_payment(
    razorpay_order_id,
    razorpay_payment_id,
    razorpay_signature
):

    msg = razorpay_order_id + "|" + razorpay_payment_id

    generated_signature = hmac.new(
        bytes(st.secrets["RAZORPAY_KEY_SECRET"], "utf-8"),
        bytes(msg, "utf-8"),
        hashlib.sha256
    ).hexdigest()

    return generated_signature == razorpay_signature


def get_user_plan(email):

    from backend_db import get_user_plan_from_db

    return get_user_plan_from_db(email)
