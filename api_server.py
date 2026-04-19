import json
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

mcp_client: MultiServerMCPClient = None
agent = None

class ChatRequest(BaseModel):
    message: str
    thread_id: str = "1"

class ChatResponse(BaseModel):
    content: str

# class Configuration:
#     @staticmethod
#     def load_servers() -> dict:
#         cfg_path = Path(__file__).with_name("servers_config.json")
#         with cfg_path.open("r", encoding="utf-8") as f:
#             return json.load(f)["mcpServers"]
        
class Configuration:
    """Configuration loader for MCP servers"""
    @staticmethod
    def load_servers():
        """Load MCP server configurations from a JSON file"""
        config_path = Path(__file__).parent / "mcp_servers_config.json"
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, "r") as f:
            config = json.load(f)
        
        return config.get("servers", [])
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI lifespan manager"""
    global mcp_client, agent
    #1. reade in MCP config
    servers_cfg = Configuration.load_servers()

    #2. connect to MCP servers and get the tools
    mcp_client = MultiServerMCPClient(servers_cfg)
    tools = await mcp_client.get_tools()

    #3. Initialize ReAct Agent
    model =  'gemini-1.5-flash' #TODO: specify the language model you want to use, e.g., "gpt-4"
    checkpointer = InMemorySaver() #keep chat history in memory

    agent = create_react_agent(
        model=model,
        tools=tools,
        checkpointer=checkpointer
    )
    yield
    await mcp_client.cleanup()
    # await mcp_client.close()

    app = FastAPI(lifespan=lifespan)

    @app.post("/chat")
    async def chat_endpoint(request: ChatRequest):
        """chat interface"""
        result = await agent.ainvoke(
            {"messages":[HumanMessage(content=request.message)]},
            {"configurable":{"thread_id": request.thread_id}}
        )

        return ChatResponse(content=result["messages"][-1].content)