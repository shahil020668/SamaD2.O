import streamlit as st
from langgraph_backaened import chatbot
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# with st.chat_message('assistant'):
#     st.text("hi")

CONFIG = {"configurable": {"thread_id": "chat-1"}}

if 'messages_history' not in st.session_state:
    st.session_state['messages_history'] = []

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

