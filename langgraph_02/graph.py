from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, START, END
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.types import interrupt
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

# this tool is wait for human assistant to response so graph will be interrupted
# and wait for human assistant to response
@tool
def human_assistant_tool(query: str):
    """Human assistant tool"""
    human_res = interrupt({"query": query}) # graph will exist after save in db 
    return human_res["data"] # resume when they get the response

tools = [human_assistant_tool]

foo = init_chat_model(model_provider="google_genai", model="gemini-2.0-flash", google_api_key=os.getenv("GEMINI_API_KEY"))

llm = foo.bind_tools(tools)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    messages = state.get("messages")
    res = llm.invoke(messages)
    return { "messages": [res]}

graph_builder = StateGraph(State)

tool_node = ToolNode(tools=tools)

graph_builder.add_node("tools", tool_node)
graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()    

def create_chat_graph(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)