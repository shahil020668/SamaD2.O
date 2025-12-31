import streamlit as st
from streamlit_option_menu import option_menu
import app




class MultiApp:

    def __init__(self):
        self.apps = []

    def add_apps(self,function):
        self.apps.append({
            "function" : function
        })
    
    def run():

        with st.sidebar:
            st.markdown("""
                <style>
                [data-testid="stSidebar"] > div:first-child {
                    display: flex;
                    flex-direction: column;
                    height: 100vh;
                }
                .sidebar-spacer {
                    flex-grow: 1;
                }
                </style>
                """, unsafe_allow_html=True)



            selected = option_menu(
                None,
                ["Chat", "My Chats", "Settings", "Logout"],
                icons=["chat", "collection", "gear", "box-arrow-right"],
                styles={
                    "container": {"padding": "0!important"},
                    "nav-link": {"font-size": "15px"},
                }
            )


        if selected == "Chat":
            app.app()

        # st.write("Selected:", selected)

    run()

