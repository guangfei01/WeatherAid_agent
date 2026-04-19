import asyncio
import json
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient
# from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

prompt = "You are WeatherAid, a helpful weather assistant."

cfg_path = Path(__file__).with_name("servers_config.json")
with cfg_path.open("r", encoding="utf-8") as f:
    servers_cfg = json.load(f)["mcpServers"]


async def run_chat_loop() -> None:
    """Run the main chat loop for the WeatherAid agent"""
    print("Welcome to WeatherAid! Ask me about the current weather in any city.")

    # connect to multiple MCP servers
    mcp_client = MultiServerMCPClient(servers_cfg)
    tools = await mcp_client.get_tools()

    # inialize model
    # model = 'google_genai:gemini-2.0-flash'
    model = 'anthropic:claude-haiku-4-5-20251001'
    # model = 'anthropic:claude-opus-4-1-20250805' # choose the model based on your Anthropic account tier
             #search AI to get the command to find your model

    # initialize agent with memory checkpointer
    checkpointer = InMemorySaver() #keep chat history in memory
    agent = create_react_agent(
        model = model,
        tools = tools,
        prompt = prompt,
        checkpointer = checkpointer
    )

    # chat loop
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break
        
        # Send user input to the agent and get a response
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config={"configurable":{"thread_id": "1"}}
        )
        print(f"WeatherAid: {response['messages'][-1].content}")


    # Cleanup
    await mcp_client.close()

if __name__ == "__main__":
    asyncio.run(run_chat_loop())