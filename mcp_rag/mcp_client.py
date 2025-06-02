import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import watsonx_chat_model

import argparse

import asyncio
from mcp_use import MCPAgent, MCPClient

async def main(query):
    """Run the rag agentic pipeline using a configuration file."""

    config = {
        "mcpServers": {
            "http": {
                "url": "http://localhost:8081/sse"
            }
        }
    }

    # Create MCPClient from config file
    client = MCPClient.from_dict(config)

    # Create LLM
    llm = watsonx_chat_model()

    # Create agent with the client
    agent = MCPAgent(llm=llm, client=client, max_steps=30)

    try:
        # Run the query
        result = await agent.run(
            query,
            max_steps=30,
        )
        print("\nResult: {}".format(result))
    finally:
        # Ensure we clean up resources properly
        if client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a query with Agentic RAG.")
    parser.add_argument("query", type=str, help="The query to process")
    args = parser.parse_args()

    asyncio.run(main(args.query)) 
