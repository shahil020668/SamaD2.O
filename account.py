import streamlit as st
import requests
import firebase_admin
from firebase_admin import credentials, auth
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("FIREBASE_API_KEY") or st.secrets["FIREBASE_API_KEY"]

cred = credentials.Certificate("/home/shahil/U23CS120/LANGGRAPH/samad-efcd8-37c743f3548a.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)


def firebase_login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        return r.json()
    raise Exception(r.json()["error"]["message"])

def firebase_signup(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        return r.json()
    raise Exception(r.json()["error"]["message"])


st.title("🔥 Firebase Auth (Real Login & Signup)")

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    choice = st.selectbox("Choose action", ["Login", "Sign Up"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button(choice):
        try:
            if choice == "Login":
                data = firebase_login(email, password)
                
            else:
                data = firebase_signup(email, password)

            decoded = auth.verify_id_token(data["idToken"])
            st.session_state.user = decoded
            st.success(f"{choice} successful")

        except Exception as e:
            st.error(f"{choice} failed: {e}")

else:
    st.success("Logged in")
    st.write("UID:", st.session_state.user["uid"])
    st.write("Email:", st.session_state.user["email"])

    if st.button("Logout"):
        st.session_state.user = None
