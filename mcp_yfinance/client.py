import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import watsonx_chat_model
import asyncio
import json

# Initialize a language model (LLM)
llm = watsonx_chat_model()

# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from textwrap import dedent

def extract_agent_response_info(response):
    result = {
        'message_count': len(response['messages']),
        'messages': []
    }
    
    for message in response['messages']:
        message_info = {
            'type': message.__class__.__name__,
            'content': message.content,
            'id': getattr(message, 'id', None)
        }
        
        # Add tool call info if present
        if hasattr(message, 'tool_calls') and message.tool_calls:
            message_info['tool_calls'] = []
            for tool_call in message.tool_calls:
                message_info['tool_calls'].append({
                    'name': tool_call.get('name'),
                    'args': tool_call.get('args'),
                    'id': tool_call.get('id')
                })
        
        # Add tool message specific data
        if message.__class__.__name__ == 'ToolMessage':
            message_info['tool_name'] = message.name
            message_info['status'] = message.status
            message_info['tool_call_id'] = message.tool_call_id
            
        result['messages'].append(message_info)
        
    return result

server_params = StdioServerParameters(
    command="/Users/sourav/workstuffs/env_exp/bin/python",
    # Make sure to update to the full absolute path to your server.py file
    args=["/Users/sourav/workstuffs/mcp-projects/mcp_yfinance/server.py"],
)

async def run_agent(query):
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
            prompt = """Answer for this query - {query}

            IMPORTANT: Once you have reached to the final answer, you MUST complete the task by providing the final answer in this exact format:
            
            Final Answer: [Your response]
            
            Give answer in max 20 steps. Do not get stuck in a loop.
            """
            
            try:
                agent_response = await agent.ainvoke({"messages": dedent(prompt.format(query=query))})
                return agent_response
            except Exception as e:               
                return f"Error running agent: {str(e)}"

if __name__ == "__main__":
    # Example 1: Get IBM stock price
    query = "What is the current stock price of IBM?"
    print(f"\n##### for query: {query} #####")
    print(extract_agent_response_info(asyncio.run(run_agent(query))))

    # Example 2: Compare IBM and Apple
    query = "Compare the stock prices of IBM and Apple."
    print(f"\n##### for query: {query} #####")
    print(extract_agent_response_info(asyncio.run(run_agent(query))))

    # Example 3: Get News
    query = "What are the recent news on the stock of top five company."
    print(f"\n##### for query: {query} #####")
    print(extract_agent_response_info(asyncio.run(run_agent(query))))
    
    # Example 4 : Summarize key financial metrics and analysis for
    query = "Analyze the key financial metrics for IBM."
    print(f"\n##### for query: {query} #####")
    print(extract_agent_response_info(asyncio.run(run_agent(query))))