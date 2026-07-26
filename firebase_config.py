import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyCIjE_dAgMtP_-MuZxORz0Zp6eAG2mfd-8",
    "authDomain": "careerpilot-ai-prod.firebaseapp.com",
    "projectId": "careerpilot-ai-prod",
    "storageBucket": "careerpilot-ai-prod.firebasestorage.app",
    "messagingSenderId": "1065454730693",
    "appId": "1:1065454730693:web:9b00d272629c912a599fac",
    "databaseURL": ""

}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
