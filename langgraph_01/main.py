from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# state
class State(TypedDict):
    user_message: str
    is_coding_question: bool
    ai_response: str

# ai will decide user message is a coding question or not
def detect_query(state: State):
    messages = [
        ("system", "You are a helpful assistant in detecting the user query is coding, programming or other. if is a coding question or programming then return True else False. eg. what is python? return True, what is the sun? return False"),
        ("human", state["user_message"]),
    ]
    res = llm.invoke(messages)
    state["is_coding_question"] = res.content
    return state

# we call ai to get a coding response
def get_coding_response(state: State):
    messages = [
        ("system", "You are a helpful Coding assistant. to response user query that they are asking"),
        ("human", state["user_message"]),
    ]
    res = llm.invoke(messages)
    state["ai_response"] = res.content
    return state

# we call ai to get a non-coding response
def get_non_coding_response(state: State):
    messages = [
        ("system", "You are a helpful assistant. to response user query what they are asking but not coding"),
        ("human", state["user_message"]),
    ]
    res = llm.invoke(messages)
    state["ai_response"] = res.content
    return state

# condition edges based on the state of the graph
# also in conditional edges we have to define the return type this langraph bug so we have to define
def route_edge(state: State) -> Literal["get_coding_response", "get_non_coding_response"]:
    if state.get("is_coding_question"):
        return "get_coding_response"
    else:
        return "get_non_coding_response"

graph_builder = StateGraph(State)

# define the nodes
graph_builder.add_node("detect_query", detect_query)
graph_builder.add_node("get_coding_response", get_coding_response)
graph_builder.add_node("get_non_coding_response", get_non_coding_response)

# define the edges
graph_builder.add_edge(START, "detect_query")
# now add conditional edges based on the state of the graph
graph_builder.add_conditional_edges("detect_query", route_edge)

graph_builder.add_edge("get_coding_response", END)
graph_builder.add_edge("get_non_coding_response", END)

graph = graph_builder.compile()

def main(user_mess: str):
    state = {
        "user_message": user_mess,
        "is_coding_question": False,
        "ai_response": ""
    }
    result = graph.invoke(state)
    print(result.get("ai_response"))

while True:
    print("<========================>")
    user_mess = input("Enter your message: ")
    main(user_mess)