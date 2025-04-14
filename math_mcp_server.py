from mcp.server.fastmcp import FastMCP
# Initialize an MCP server and give it a name (for identification)
mcp_server = FastMCP("Math Tools")

@mcp_server.tool()
def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    return a + b

@mcp_server.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers and return the result."""
    return a * b

if __name__ == "__main__":
    # Start the MCP server in stdio mode (runs until program exits).
    mcp_server.run(transport="stdio")