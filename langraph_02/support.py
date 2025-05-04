from graph import create_chat_graph
from langgraph.checkpoint.mongodb import MongoDBSaver
from langgraph.types import Command

MONGODB_URI = "mongodb://localhost:27017/" 
config = {"configurable": {"thread_id": "50"}}  

def main():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph_with_mongo = create_chat_graph(checkpointer)

        data = graph_with_mongo.get_state(config=config)

        for event in data.values['messages']:
            # event.pretty_print()
            pass
        
        last_message = data.values['messages'][-1]
        print("Last message:", last_message)

        tool_calls = getattr(last_message, "tool_calls", [])
        print("Tool calls:", tool_calls)

        user_query = None   
        for call in tool_calls:
            if call.get("name") == "human_assistant_tool":
                args = call.get("args", {})
                user_query = args.get("query")

        print("User query:", user_query)
        human_assistant_input = input("Ans ->")

        resume_command = Command(resume={"data": human_assistant_input})
        for event in graph_with_mongo.stream(resume_command, config, stream_mode="values"):
            if "messages" in event:
                event["messages"][-1].pretty_print() 

main()