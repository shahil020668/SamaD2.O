import os
from dotenv import load_dotenv
from streamlit_cookies_manager import EncryptedCookieManager

load_dotenv()

cookies = EncryptedCookieManager(
    prefix="samad/",
    password=os.getenv("COOKIE_SECRET")
)

def init_cookies():
    if not cookies.ready():
        return False
    return True
