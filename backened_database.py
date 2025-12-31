from langgraph.graph import StateGraph, START, END
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id='deepseek-ai/DeepSeek-V3.2',
    task='text-generation'
    
)

llm1 = HuggingFaceEndpoint(
    repo_id='meta-llama/Llama-4-Scout-17B-16E-Instruct',
    task='text-generation'
)

# model = ChatGoogleGenerativeAI(model='gemma-3-12b')

model = ChatHuggingFace(llm=llm)

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]


def initialize(state: ChatState):
    return {
        "messages": [
            SystemMessage(
                content=""" """
            )
        ]
    }


def chat_node(state : ChatState):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages" : [response]}


# checkpointer

checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("initialize", initialize)

graph.add_edge(START, "initialize")
graph.add_edge("initialize", "chat_node")
graph.add_edge("chat_node",END)


chatbot = graph.compile(checkpointer=checkpointer)

# initial_state = {
#     'messages' : [HumanMessage (content = 'what is my name')]
# }
# final_state = chatbot.invoke(initial_state,config={"configurable": {"thread_id": "chat-1"}})

# print(chatbot.get_state(config={"configurable": {"thread_id": "chat-1"}}).values)
# print(final_state)
all_thread = set()
def fetch_all_thread():
    for cp in checkpointer.list(None):
        all_thread.add(cp.config["configurable"]["thread_id"])

    return (list(all_thread))