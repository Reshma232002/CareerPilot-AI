import os
import hmac
import hashlib
from datetime import datetime, timedelta

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv

import razorpay

import firebase_admin
from firebase_admin import credentials, firestore


# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()


RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")


# =====================================================
# FIREBASE INITIALIZATION
# =====================================================

cred = credentials.Certificate("firebase_key.json")

firebase_admin.initialize_app(cred)

db = firestore.client()


# =====================================================
# RAZORPAY CLIENT
# =====================================================

client = razorpay.Client(
    auth=(
        RAZORPAY_KEY_ID,
        RAZORPAY_KEY_SECRET
    )
)


# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI(
    title="CareerPilot AI Payment Backend",
    version="1.0"
)


# Allow Streamlit frontend connection

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# TEST ROUTE
# =====================================================

@app.get("/")
def home():

    return {
        "status": "CareerPilot AI Payment Backend Running"
    }
# =====================================================
# RAZORPAY WEBHOOK
# =====================================================
@app.post("/razorpay-webhook")
async def razorpay_webhook(request: Request):

    body = await request.body()

    received_signature = request.headers.get(
        "X-Razorpay-Signature"
    )


    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()


    print("==============================")
    print("SIGNATURE MATCH:",
          received_signature == expected_signature)
    print("==============================")


    if received_signature != expected_signature:
        raise HTTPException(
            status_code=400,
            detail="Invalid webhook signature"
        )


    payload = await request.json()

    event = payload.get("event")

    print("EVENT:", event)


    if event in [
        "payment.captured",
        "order.paid"
    ]:


        payment_entity = (
            payload["payload"]
            ["payment"]
            ["entity"]
        )


        order_id = payment_entity.get(
            "order_id"
        )

        payment_id = payment_entity.get(
            "id"
        )


        if not order_id:
            return {
                "status": "No order id"
            }


        order_ref = db.collection("payments").document(order_id)


        order_doc = order_ref.get()


        if not order_doc.exists:

            print(
                "Order not found:",
                order_id
            )

            return {
                "status": "Order missing"
            }


        order_data = order_doc.to_dict()


        if order_data.get("status") == "completed":

            print(
                "Already processed"
            )

            return {
                "status": "Already completed"
            }


        email = order_data.get(
            "email"
        )

        plan = order_data.get(
            "plan",
            "premium"
        )


        if email:


            upgrade_user(
                email,
                plan
            )
            print(
                "UPGRADE COMPLETED FOR:",
                email,
                plan
            )


            order_ref.update({

                "status": "completed",

                "payment_id": payment_id,

                "completed_at":
                    datetime.utcnow()

            })


            print(
                f"SUCCESS: {email} upgraded"
            )


    return {
        "status": "Webhook received"
    }
# =====================================================
# UPDATE USER PREMIUM PLAN
# =====================================================

def upgrade_user(email, plan):

    user_id = email.replace(".", "_")

    user_ref = db.collection("users").document(user_id)

    expiry = datetime.utcnow() + timedelta(days=30)


    user_ref.set({

        "email": email,

        "plan": plan,

        "premium_expiry": expiry.isoformat(),

        "payment_status": "paid",

        "updated_at": datetime.utcnow()

    }, merge=True)


    print(
        f"{email} upgraded to {plan}"
    )

# =====================================================
# RUN SERVER
# =====================================================

# Start command:
#
# uvicorn main:app --reload
#
