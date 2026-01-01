import requests
import os
import streamlit as st
from firebase_admin import auth
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FIREBASE_API_KEY") or st.secrets["FIREBASE_API_KEY"]

def login(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"
    r = requests.post(url, json={
        "email": email,
        "password": password,
        "returnSecureToken": True
    })
    if r.status_code == 200:
        return r.json()
    raise Exception(r.json()["error"]["message"])

def signup(email, password):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
    r = requests.post(url, json={
        "email": email,
        "password": password,
        "returnSecureToken": True
    })
    if r.status_code == 200:
        return r.json()
    raise Exception(r.json()["error"]["message"])

def verify_token(id_token):
    return auth.verify_id_token(id_token)
