import streamlit as st
st.set_page_config(layout='centered')
from langgraph_backaened import chatbot
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import uuid
import firebase_admin
from firebase_admin import credentials
from auth import login, signup, verify_token
from cookies import cookies,init_cookies
from dotenv import load_dotenv
from cookies import init_cookies
from streamlit_cookies_manager.cookie_manager import CookiesNotReady


load_dotenv()

def get_token():
    try:
        return cookies.get("token")
    except CookiesNotReady:
        return None

token = get_token()


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.show_auth = False

if not st.session_state.logged_in and cookies.get("token"):
    try:

        user = verify_token(cookies["token"])
        st.session_state.user = user
        st.session_state.logged_in = True
        st.switch_page("pages/streamlit_database.py")
    except:
        cookies.pop("token")
        cookies.save()

c1, c2 = st.columns([6, 1])
with c2:
    if st.button("login/signup"):
        st.session_state.show_auth = True

if not firebase_admin._apps:
    cred = credentials.Certificate("/home/shahil/U23CS120/LANGGRAPH/samad-efcd8-37c743f3548a.json")
    firebase_admin.initialize_app(cred)

#***************************unsaves chat interface****************************************


def generate_threadid():
    threadid = uuid.uuid4()
    return threadid

if 'messages_history' not in st.session_state:
    st.session_state['messages_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_threadid()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

# when reloading 

add_thread(st.session_state['thread_id'])

CONFIG = {"configurable": {"thread_id": st.session_state['thread_id']}}

def load_conversation(thread_id):
    return chatbot.get_state(config={"configurable": {"thread_id": thread_id}}).values['messages']

def reset_chat():
    thread_id = generate_threadid()
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['messages_history'] = []

st.sidebar.title("SamaD2.O")
if st.sidebar.button("New chat"):
    reset_chat()
st.sidebar.header("My conversation")



for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
        if messages:
            st.session_state['messages_history'] = messages
        else:
            st.session_state['messages_history'] = []

    
# with st.sidebar.container():
#     st.write("Chat History")
#     st.button("Clear Chat")
#     st.text_input("Search")


st.title("💬 SamaD2.O")


for message in st.session_state['messages_history']:
    if isinstance(message, HumanMessage):
        with st.chat_message('user'):
            st.write(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message('assistant'):
            st.write(message.content)

user_input = st.chat_input('Ask anything')


def stream_ai_response(chatbot, user_input, config):
    full_response = ""

    def generator():
        nonlocal full_response
        for message_chunk, metadata in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="messages"
        ):
            if isinstance(message_chunk, AIMessage):
                full_response += message_chunk.content
                yield message_chunk.content

    st.write_stream(generator())
    return AIMessage(content=full_response)



if user_input:
    st.session_state['messages_history'].append(HumanMessage(content=user_input))
    with st.chat_message('user'):
        st.write(user_input)
    
    # result = chatbot.invoke({'messages' : [HumanMessage (content = user_input)]},config=CONFIG)
    # ai_message = result['messages'][-1]

    with st.chat_message('assistant'):
        ai_message = stream_ai_response(chatbot, user_input, CONFIG)
    st.session_state['messages_history'].append(ai_message)


@st.dialog("🔐 Login / Signup")
def auth_dialog():
    mode = st.radio(
        "Mode",
        ["Login", "Sign Up"],
        horizontal=True
    )

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("❌ Cancel"):
            st.session_state.show_auth = False
            st.rerun()

    with col2:
        if st.button(mode):
            try:
                if mode == "Login":
                    data = login(email, password)
                    user = verify_token(data["idToken"])

                    cookies["token"] = data["idToken"]
                    cookies.save()

                    st.session_state.user = user
                    st.session_state.logged_in = True
                    st.session_state.show_auth = False

                    st.switch_page("pages/streamlit_database.py")

                else:
                    signup(email, password)
                    st.success("Signup successful. Please login.")

            except Exception as e:
                st.error(e)

if st.session_state.show_auth:
    auth_dialog()