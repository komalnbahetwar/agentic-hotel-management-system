from langchain_core.tools import tool
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, create_react_agent, tools_condition
from langchain_openai import ChatOpenAI
from langgraph.graph.message import add_messages
from app.agents.tools import check_availability_tool, book_room_tool
from app.agents.tools import get_menu, order_food, get_food_bill

import os
from dotenv import load_dotenv

# Load .env file into environment
load_dotenv()

# Now you can access variables
# api_key = os.getenv("GROQ_API_KEY")            # <----- If using the Groq API

api_key = os.getenv("OPENAI_API_KEY")        # <----- If using the OpenAI API


## LLM

# llm = ChatOpenAI(                                                 # <----- If using the Groq API
#     model="openai/gpt-oss-120b",   # Groq-supported model
#     temperature=0,
#     api_key=api_key,
#     base_url="https://api.groq.com/openai/v1"
# )

llm = ChatOpenAI(model="gpt-4o", temperature=0, api_key=api_key)           # <----- If using the OpenAI API


# --- 1. Define Booking tools ---
room_booking_tools = [check_availability_tool, book_room_tool]

room_booking_system_message = """
You are a hotel booking assistant.
Required information to book a room:
- Guest name
- Room number

Your rules:
1. If any required information is missing, DO NOT call tools yet.
   Instead, ask the user for the missing information.
2. Only call `book_room_tool` once you have both guest name AND room number.
3. Use `check_availability_tool` if the user asks which rooms are free.
"""

# --- 2. Build LLM agent with tools ---
room_booking_agent = create_react_agent(llm, room_booking_tools, prompt=room_booking_system_message)


# --- 3. Graph setup ---

from typing import TypedDict, List, Optional, Annotated
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage, AIMessage

class State(TypedDict):
    messages: Annotated[list, add_messages]

# --- 4. Build graph ---
room_booking_graph_builder = StateGraph(State)

# Nodes
room_booking_graph_builder.add_node("agent", room_booking_agent)

room_booking_tool_node = ToolNode(tools=room_booking_tools)

room_booking_graph_builder.add_node("tools", room_booking_tool_node)

# Edges
room_booking_graph_builder.add_conditional_edges("agent", tools_condition)  # if tool needed, go to tools
room_booking_graph_builder.add_edge("tools", "agent")
room_booking_graph_builder.set_entry_point("agent")

from langgraph.checkpoint.memory import MemorySaver
room_booking_memory = MemorySaver()

# Compile 
room_booking_graph = room_booking_graph_builder.compile(checkpointer=room_booking_memory)

# --- 1. Define tools ---
order_food_tools = [get_menu,order_food, get_food_bill]


order_food_system_message = """
You are a hotel food ordering assistant.

Available tools:
- get_menu → Show available dishes.
- order_food → Place a food order for a guest (requires dish, quantity, and room number).
- get_food_bill → Show the food bill for a room (requires room number).

Your rules:
1. Always confirm missing required details with the guest before calling a tool.
   - For `order_food`, ask for dish name, quantity, and room number if any is missing.
   - For `get_food_bill`, ask for the room number if missing.
2. Only call a tool when all required parameters are available.
3. When showing the menu, only list available items (tool handles this).
4. After placing an order, confirm the action back to the guest.
5. Be polite and conversational while guiding the guest.
"""


# --- 2. Build LLM agent with tools ---
order_food_agent = create_react_agent(llm, order_food_tools, prompt=order_food_system_message)


# --- 3. Graph setup ---

from typing import TypedDict, List, Optional, Annotated
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage, AIMessage

class State(TypedDict):
    messages: Annotated[list, add_messages]

# --- 4. Build graph ---
order_food_graph_builder = StateGraph(State)

# Nodes
order_food_graph_builder.add_node("agent", order_food_agent)

order_food_tool_node = ToolNode(tools=order_food_tools)

order_food_graph_builder.add_node("tools", order_food_tool_node)

# Edges
order_food_graph_builder.add_conditional_edges("agent", tools_condition)  # if tool needed, go to tools
order_food_graph_builder.add_edge("tools", "agent")
order_food_graph_builder.set_entry_point("agent")

from langgraph.checkpoint.memory import MemorySaver
order_food_memory = MemorySaver()

# Compile 
order_food_graph = order_food_graph_builder.compile(checkpointer=order_food_memory)




@tool
def booking_agent_tool(messages: list) -> str:
    """Interact with the booking agent"""
    print(" **** CALLING Agent: booking_agent *******")

    response = room_booking_graph.invoke({"messages": messages})
    return response["messages"][-1].content

@tool
def food_agent_tool(messages: list) -> str:
    """Interact with the food ordering agent"""
    print(" **** CALLING Agent: food_agent *******")

    response = order_food_graph.invoke({"messages": messages})
    return response["messages"][-1].content



supervisor_tools = [booking_agent_tool, food_agent_tool]

supervisor_system_message = """
You are the hotel concierge agent.
- For room related queries, call `booking_agent_tool`.
- For food related queries, call `food_agent_tool`.
- Keep the conversation natural.
"""

supervisor_agent = create_react_agent(llm, supervisor_tools, prompt=supervisor_system_message)


from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated

class State(TypedDict):
    messages: Annotated[list, add_messages]

supervisor_graph_builder = StateGraph(State)

supervisor_graph_builder.add_node("supervisor_agent", supervisor_agent)
supervisor_tool_node = ToolNode(tools=supervisor_tools)
supervisor_graph_builder.add_node("tools", supervisor_tool_node)

supervisor_graph_builder.add_conditional_edges("supervisor_agent", tools_condition)
supervisor_graph_builder.add_edge("tools", "supervisor_agent")
supervisor_graph_builder.set_entry_point("supervisor_agent")

