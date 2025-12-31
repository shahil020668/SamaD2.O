import streamlit as st
from backened_database import chatbot, fetch_all_thread
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import uuid
import time

def generate_threadid() -> str:
    threadid = uuid.uuid4()
    return f"chat_{len(fetch_all_thread())+1}"

if 'messages_history' not in st.session_state:
    st.session_state['messages_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_threadid()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = fetch_all_thread()

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

