from graph import create_chat_graph
from langgraph.checkpoint.mongodb import MongoDBSaver

MONGODB_URI = "mongodb://localhost:27017/" 
config = {"configurable": {"thread_id": "50"}}  

def main():
    with MongoDBSaver.from_conn_string(MONGODB_URI) as checkpointer:
        graph_with_mongo = create_chat_graph(checkpointer)

        while True:
            user_inp = input("> ")
            for event in graph_with_mongo.stream({"messages": [{"role": "user", "content": user_inp}]}, config, stream_mode="values"):
                if "messages" in event:
                    event["messages"][-1].pretty_print()
                
main()