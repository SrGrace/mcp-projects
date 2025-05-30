# mcp-projects

Open-Source Projects Repo for MCP (Model Context Protocol).

## Steps to install and run:

1. Clone this repo
2. Install the requirements
    ```
    pip install mcp fastapi uvicorn fastapi-mcp llama-index llama-index-embeddings-huggingface llama-index-llms-langchain langchain-mcp-adapters mcp-use
    ```
3. Make a .env file in the root folder with the following credentials:
    ```
    API_KEY=<IBM_cloud_API_Key>
    PROJECT_ID=<Watsonx_Project_id>
    IBM_CLOUD_URL=<IBM cloud url>

    MODEL_ID=<your watsonx.ai LLM id>

    TAVILY_API_KEY=<your Tavily api key for web search>

    or, use your own llm provider - its agnostic to the projects (few changes needs to be done though)
    ```
4. Experiment with different projects and files
    - make sure to run the mcp servers first and then only
    - run the clients


## What is Model Context Protocol (MCP)?
At its core, MCP is a standardized way for applications to provide AI models with richer context about their environment, user preferences, and conversation history. Think of it as a smart, structured way to feed memory and context to AI systems.

![MCP Structure](./data/mcp%20structure.png)

### The Problem MCP Solves
Current AI systems have limited "working memory" - they can only see a certain amount of conversation history at once (their "context window"). Imagine trying to have a conversation with someone who only remembers the last few exchanges:
- You: "Remember that project we discussed last week about optimizing the supply chain?"
- AI without good context: "I don't recall that specific discussion. Could you remind me of the details?"
- 
This limitation forces users to constantly re-explain things, leading to frustrating interactions. MCP aims to solve this by creating a structured method for maintaining and accessing context.

### Some Analogies
**1. GPS Navigation**

Traditional AI context management is like giving someone directions one turn at a time, without showing them the full map. If they forget a step, the journey breaks down.
  
MCP is like a GPS navigation system that:
- Knows your destination
- Remembers your preferred routes
- Adjusts based on real-time conditions
- Always knows exactly where you are in the journey

Read this medium article for comprehensive understanding of MCP: [Understanding Model Context Protocol (MCP): A Layman’s Guide](https://medium.com/@SrGrace_/understanding-model-context-protocol-mcp-a-laymans-guide-4737aab5fc6b)


`Do make Pull Requests to contribute to this asset ✨`
