from fastapi import APIRouter
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.agents.supervisor_agent import supervisor_graph_builder

# memory for supervisor agent
from langgraph.checkpoint.memory import MemorySaver

supervisor_memory = MemorySaver()

supervisor_graph = supervisor_graph_builder.compile(checkpointer= supervisor_memory)

router = APIRouter()

class ChatRequest(BaseModel):
    thread_id: str
    user_message: str

chat_histories = {}

@router.post("/chat")
def chat(req: ChatRequest):
    history = chat_histories.get(req.thread_id, [])
    history.append(HumanMessage(content=req.user_message))

    conf = {"configurable": {"thread_id": req.thread_id}}
    
    response = supervisor_graph.invoke(
        {"messages": [HumanMessage(content=req.user_message)]}, conf
    )

    history.append(response["messages"][-1])
    chat_histories[req.thread_id] = history

    return {"reply": response["messages"][-1].content}


