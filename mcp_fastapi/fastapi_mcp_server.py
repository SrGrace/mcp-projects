from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
import uvicorn

app = FastAPI()

mcp = FastApiMCP(
    app,
    # Optional parameters
    name="My API MCP",
    description="My API description",
    base_url="http://localhost:8000",
)

# Mount the MCP server directly to your FastAPI app
mcp.mount()

# Add new endpoints after MCP server creation
@app.get("/new/endpoint/", operation_id="new_endpoint")
async def new_endpoint():
    return {"message": "Hello, world!"}

# Refresh the MCP server to include the new endpoint
mcp.setup_server()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
