from fastapi import FastAPI
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain.agents import initialize_agent
from langchain_mcp_adapters.tools import load_mcp_tools

import os
from dotenv import load_dotenv
load_dotenv(override=True)

from langchain_ibm import ChatWatsonx
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

def watsonx_model(model_id="meta-llama/llama-3-3-70b-instruct", decoding_method='greedy', max_new_tokens=8192, 
                  min_new_tokens=1, temperature=0.5, top_k=50, top_p=1, repetition_penalty=1):
    params = {
        GenParams.DECODING_METHOD: decoding_method,
        GenParams.MIN_NEW_TOKENS: min_new_tokens,
        GenParams.MAX_NEW_TOKENS: max_new_tokens,
        GenParams.RANDOM_SEED: 42,
        GenParams.TEMPERATURE: temperature,
        GenParams.TOP_K: top_k,
        GenParams.TOP_P: top_p,
        GenParams.REPETITION_PENALTY: repetition_penalty
    }
    ibm_cloud_url = os.getenv("IBM_CLOUD_URL", None)
    project_id = os.getenv("PROJECT_ID", None)
    api_key = os.getenv("API_KEY")
    watsonx_llm = ChatWatsonx(
        model_id=model_id,
        url=ibm_cloud_url,
        apikey=api_key,
        project_id=project_id,
        params=params,
    )
    return watsonx_llm


# We'll assume the MCP server code from Step 1 is saved as math_mcp_server.py
server_params = StdioServerParameters(
    command="/Users/sourav/workstuffs/env_exp/bin/python",
    args=["/Users/sourav/workstuffs/mcp-projects/math_mcp_server.py"]  # launch our MCP server script
)

# Start the MCP client and load the tools from the server
async def init_tools():
    # Connect to the MCP server via stdio transport
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()            # handshake with server
            tools = await load_mcp_tools(session) # fetch available tools (add, multiply)
            return tools
            
# Initialize the tools (run the async setup synchronously at startup)
mcp_tools = init_tools()
 
# Initialize a language model (LLM) and an agent that can use the MCP tools
llm = watsonx_model()
agent = initialize_agent(mcp_tools, llm, agent="zero-shot-react-description", verbose=True)

# Set up FastAPI app
app = FastAPI()

@app.post("/chat")
def chat(query: str):
    """Take a user query and return the chatbot's answer (using MCP tools as needed)."""
    answer = agent.run(query)
    return {"answer": answer}

# To run the server: uvicorn this_file_name:app --reload