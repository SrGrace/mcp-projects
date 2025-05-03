import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import watsonx_chat_model

# Initialize a language model (LLM)
llm = watsonx_chat_model()

# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent


import asyncio

server_params = StdioServerParameters(
    command="/Users/sourav/workstuffs/env_exp/bin/python",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["/Users/sourav/workstuffs/mcp-projects/mcp_maths/mcp_server.py"],
)

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create agent with termination condition
            agent = create_react_agent(
                llm, 
                tools,
            )

            # Modify the prompt to encourage termination
            prompt = """Solve this math problem step by step: what's (3 + 5) x 12?

            IMPORTANT: Once you have calculated the final answer, you MUST complete the task by providing the final answer in this exact format:
            
            Final Answer: [Your calculated result]
            
            Do not get stuck in a loop of calculations. 
            """
            
            try:
                agent_response = await agent.ainvoke({"messages": prompt})
                return agent_response
            except Exception as e:
                print(f"Error type: {type(e).__name__}")
                print(f"Error running agent: {str(e)}")
                
                return f"Error running agent: {str(e)}"


# Run the async function
if __name__ == "__main__":
    result = asyncio.run(run_agent())
    print(result)
