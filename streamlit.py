import streamlit as st
from langgraph_backaened import chatbot
from langchain_core.messages import HumanMessage

# with st.chat_message('assistant'):
#     st.text("hi")

CONFIG = {"configurable": {"thread_id": "chat-1"}}

if 'messages_history' not in st.session_state:
    st.session_state['messages_history'] = []


for message in st.session_state['messages_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Ask anything')

if user_input:
    st.session_state['messages_history'].append({'role' : 'user', 'content' : user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    result = chatbot.invoke({'messages' : [HumanMessage (content = user_input)]},config=CONFIG)
    ai_message = result['messages'][-1].content
    st.session_state['messages_history'].append({'role' : 'assistant', 'content' : ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)
