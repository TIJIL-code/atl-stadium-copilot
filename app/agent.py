import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool

load_dotenv()

@tool
def check_live_gate_congestion() -> str:
    """Fetches real-time passenger flow rates and wait times at all stadium gates."""
    try:
        data = requests.get("http://127.0.0.1:8000/api/v1/gates").json()
        return str(data)
    except Exception:
        return "Error: Unable to connect to the Live Gate Telemetry API."

@tool
def check_marta_transit_status() -> str:
    """Checks live crowd capacity and platform holding statuses for nearby MARTA rail lines."""
    try:
        data = requests.get("http://127.0.0.1:8000/api/v1/transit").json()
        return str(data)
    except Exception:
        return "Error: Unable to connect to the Transit Logistics API."

@tool
def check_stadium_weather_and_roof() -> str:
    """Retrieves live meteorological data and current open/closed state of the retractable roof."""
    try:
        data = requests.get("http://127.0.0.1:8000/api/v1/weather").json()
        return str(data)
    except Exception:
        return "Error: Unable to connect to the Climate Sensor API."

tools = [check_live_gate_congestion, check_marta_transit_status, check_stadium_weather_and_roof]

def get_ops_agent():
    llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are the Atlanta Stadium (Mercedes-Benz Stadium) AI Operations Copilot for FIFA 2026.\n"
            "Your job is to provide real-time decision support for venue managers.\n"
            "Rules:\n"
            "1. Always check live telemetry tools before answering logistical or environmental questions.\n"
            "2. Be concise, hyper-focused on public safety, and format responses with clear action points."
        )),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)