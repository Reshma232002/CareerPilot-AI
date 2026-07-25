from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# ======================================
# Firebase Initialization
# ======================================
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ======================================
# SAVE RESUME ANALYSIS
# ======================================
def save_analysis(
    user_email,
    resume_text,
    job_description,
    ats_score,
    matched_skills,
    missing_skills,
    cover_letter,
    linkedin_summary,
    ai_insights,
):

    db.collection("resume_analyses").add({
        "user_email": user_email,
        "resume_text": resume_text,
        "job_description": job_description,
        "ats_score": ats_score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "cover_letter": cover_letter,
        "linkedin_summary": linkedin_summary,
        "ai_insights": ai_insights,
        "created_at": firestore.SERVER_TIMESTAMP,
    })


# ======================================
# HISTORY
# ======================================
def get_user_history(user_email):

    docs = (
        db.collection("resume_analyses")
        .where("user_email", "==", user_email)
        .stream()
    )

    return [doc.to_dict() for doc in docs]


# ======================================
# DASHBOARD
# ======================================
def get_dashboard_stats(user_email):

    docs = (
        db.collection("resume_analyses")
        .where("user_email", "==", user_email)
        .stream()
    )

    analyses = [doc.to_dict() for doc in docs]

    if not analyses:
        return {
            "total": 0,
            "avg_score": 0,
            "max_score": 0
        }

    scores = [item.get("ats_score", 0) for item in analyses]

    return {
        "total": len(scores),
        "avg_score": round(sum(scores) / len(scores), 2),
        "max_score": max(scores)
    }


# ======================================
# USER FUNCTIONS
# ======================================
def get_user_doc(user_email):

    doc_ref = db.collection("users").document(
        user_email.replace(".", "_")
    )

    doc = doc_ref.get()

    return doc.to_dict() if doc.exists else {}


def get_user_usage(user_email):

    user_doc = get_user_doc(user_email)

    return int(user_doc.get("daily_usage", 0))


# ======================================
# UPDATE USAGE
# ======================================
def increment_usage(user_email):

    try:

        user_ref = db.collection("users").document(
            user_email.replace(".", "_")
        )

        user_doc = user_ref.get()

        current_daily = 0
        current_total = 0

        if user_doc.exists:
            data = user_doc.to_dict()

            current_daily = data.get("daily_usage", 0)
            current_total = data.get("total_usage", 0)

        user_ref.set(
            {
                "daily_usage": current_daily + 1,
                "total_usage": current_total + 1,
                "last_reset": datetime.now().date().isoformat(),
                "updated_at": firestore.SERVER_TIMESTAMP,
            },
            merge=True
        )

    except Exception as e:
        print("Firestore Error:", str(e))


# ======================================
# RESET DAILY USAGE
# ======================================
def reset_daily_usage_if_needed(user_email):

    user_ref = db.collection("users").document(
        user_email.replace(".", "_")
    )

    user_doc = user_ref.get()

    if not user_doc.exists:
        return

    user = user_doc.to_dict()

    last_reset = user.get("last_reset")

    today = datetime.now().date().isoformat()

    if last_reset != today:

        user_ref.set(
            {
                "daily_usage": 0,
                "last_reset": today,
                "updated_at": firestore.SERVER_TIMESTAMP,
            },
            merge=True
        )


# ======================================
# USER PLAN
# ======================================
def get_user_plan_from_db(user_email):

    user_doc = get_user_doc(user_email)

    return user_doc.get("plan", "free")


# ======================================
# CREATE USER
# ======================================
def create_user_if_not_exists(user_email):

    user_ref = db.collection("users").document(
        user_email.replace(".", "_")
    )

    if not user_ref.get().exists:

        user_ref.set({

            "email": user_email,

            "plan": "free",

            "role": "user",

            "daily_usage": 0,
            "total_usage": 0,

            "resume_analysis_count": 0,
            "resume_builder_count": 0,
            "career_planner_count": 0,
            "career_dna_count": 0,
            "learning_roadmap_count": 0,
            "skill_gap_count": 0,
            "job_matcher_count": 0,
            "interview_count": 0,
            "copilot_count": 0,
            "job_application_count": 0,
            "interview_tracker_count": 0,

            "last_login": firestore.SERVER_TIMESTAMP,
            "last_reset": datetime.now().date().isoformat(),

            "created_at": firestore.SERVER_TIMESTAMP,
            "updated_at": firestore.SERVER_TIMESTAMP,

        })


# ======================================
# UPDATE LAST LOGIN
# ======================================
def update_last_login(user_email):

    db.collection("users").document(
        user_email.replace(".", "_")
    ).set(
        {
            "last_login": firestore.SERVER_TIMESTAMP,
            "updated_at": firestore.SERVER_TIMESTAMP,
        },
        merge=True
    )
# ======================================
# UPDATE FEATURE COUNTER
# ======================================
def increment_feature_count(user_email, feature_name):

    user_ref = db.collection("users").document(
        user_email.replace(".", "_")
    )

    doc = user_ref.get()

    if not doc.exists:
        return

    data = doc.to_dict()

    current = data.get(feature_name, 0)

    user_ref.set(
        {
            feature_name: current + 1,
            "updated_at": firestore.SERVER_TIMESTAMP
        },
        merge=True
    )    
    # ======================================
# ADMIN DASHBOARD STATS
# ======================================

def get_admin_dashboard_stats():

    users = list(db.collection("users").stream())

    analyses = list(db.collection("resume_analyses").stream())

    total_users = len(users)

    premium_users = 0

    recruiter_users = 0

    total_usage = 0

    total_resume_analyses = len(analyses)

    for user in users:

        data = user.to_dict()

        plan = data.get("plan", "free")

        if plan == "premium":
            premium_users += 1

        elif plan == "recruiter":
            recruiter_users += 1

        total_usage += data.get("total_usage", 0)

    return {

        "total_users": total_users,

        "premium_users": premium_users,

        "recruiter_users": recruiter_users,

        "total_resume_analyses": total_resume_analyses,

        "total_usage": total_usage

    }
# ======================================
# RECRUITER DASHBOARD
# ======================================

def get_all_resume_analyses():

    docs = db.collection(
        "resume_analyses"
    ).stream()

    analyses = []

    for doc in docs:

        analyses.append(doc.to_dict())

    return analyses
# ======================================
# JOB TRACKER
# ======================================

def save_job_application(
    user_email,
    company,
    role,
    location,
    applied_date,
    status,
    notes,
):

    db.collection("job_applications").add({

        "user_email": user_email,

        "company": company,

        "role": role,

        "location": location,

        "applied_date": applied_date,

        "status": status,

        "notes": notes,

        "created_at": firestore.SERVER_TIMESTAMP

    })


def get_job_applications(user_email):

    docs = (

        db.collection("job_applications")

        .where("user_email", "==", user_email)

        .stream()

    )

    return [doc.to_dict() for doc in docs]

# ======================================
# APPLICATION TRACKER
# ======================================

def save_application_status(
    user_email,
    company,
    role,
    stage,
    notes,
):

    db.collection("application_tracker").add({

        "user_email": user_email,

        "company": company,

        "role": role,

        "stage": stage,

        "notes": notes,

        "created_at": firestore.SERVER_TIMESTAMP

    })


def get_application_statuses(user_email):

    docs = (

        db.collection("application_tracker")

        .where("user_email", "==", user_email)

        .stream()

    )

    return [doc.to_dict() for doc in docs]
# ==================================================
# USER PROFILE
# ==================================================

def save_user_profile(email, profile_data):

    db.collection("users").document(email.replace(".", "_")).set(
        profile_data,
        merge=True
    )


def get_user_profile(email):

    doc = db.collection("users").document(
        email.replace(".", "_")
    ).get()

    if doc.exists:
        return doc.to_dict()

    return {}

from datetime import datetime


# ==================================================
# ADD NOTIFICATION
# ==================================================

def add_notification(user_email, title, message):

    doc_ref = db.collection("users").document(
        user_email.replace(".", "_")
    )

    doc = doc_ref.get()

    if doc.exists:

        data = doc.to_dict()

        notifications = data.get("notifications", [])

    else:

        notifications = []

    notifications.append({

        "title": title,

        "message": message,

        "read": False,

        "time": datetime.now().strftime("%d %b %Y %I:%M %p")

    })

    doc_ref.set(

        {

            "notifications": notifications,

            "updated_at": firestore.SERVER_TIMESTAMP

        },

        merge=True

    )

# ==================================================
# GET NOTIFICATIONS
# ==================================================

def get_notifications(user_email):

    doc = get_user_doc(user_email)

    return doc.get("notifications", [])


# ==================================================
# MARK ALL READ
# ==================================================

def mark_notifications_read(user_email):

    doc_ref = db.collection("users").document(
        user_email.replace(".", "_")
    )

    doc = doc_ref.get()

    if not doc.exists:
        return

    data = doc.to_dict()

    notifications = data.get("notifications", [])

    for item in notifications:
        item["read"] = True

    doc_ref.set(
        {
            "notifications": notifications
        },
        merge=True
    )


# ==================================================
# CLEAR NOTIFICATIONS
# ==================================================

def clear_notifications(user_email):

    db.collection("users").document(
        user_email.replace(".", "_")
    ).set(
        {
            "notifications": []
        },
        merge=True
    )    

# ==================================================
# GET UNREAD NOTIFICATION COUNT
# ==================================================

def get_unread_notification_count(user_email):

    notifications = get_notifications(user_email)

    count = 0

    for item in notifications:

        if not item.get("read", False):
            count += 1

    return count    

# ======================================
# USER ROLE
# ======================================

def get_user_role(user_email):

    user = get_user_doc(user_email)

    return user.get("role", "user")