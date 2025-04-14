import os
from dotenv import load_dotenv
load_dotenv(override=True)

import asyncio
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
from rag import RAGWorkflow

import nest_asyncio
nest_asyncio.apply()

mcp = FastMCP(
    "MCP-RAG-APP",
    host="127.0.0.1",
    port=8080,
    timeout=30
)

tavily_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
rag_workflow = RAGWorkflow()

@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for the given query."""
    search_response = tavily_client.search(
        query=query,
        max_results=3
    )
    return search_response

@mcp.tool()
async def rag(query: str) -> str:
    """Use RAG workflow to answer queries about Deep Seek"""
    response = await rag_workflow.query(query)
    return str(response)


if __name__ == "__main__":
    asyncio.run(rag_workflow.ingest_documents("data"))
    mcp.run(transport="stdio")
