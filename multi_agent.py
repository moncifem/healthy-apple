from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    WebSearchTool,
    MCPClient,
    LiteLLMModel,
)
from tool import visit_webpage
from sql_agent import create_sql_agent, SERVER_PARAMETERS
from visual_agent import visual_agent

model = LiteLLMModel(model_id="anthropic/claude-sonnet-4-20250514", temperature=0.2)

web_agent = ToolCallingAgent(
    tools=[WebSearchTool(), visit_webpage],
    model=model,
    max_steps=1,
    name="web_search_agent",
    description="Runs web searches for you.",
)
web_agent.prompt_templates["system_prompt"] = (
    """You are a web search agent. Your job is to run web searches and visit webpages to find information for the user. When you make a websearch, make sure to ONLY use a few keywords."""
)


def create_main_agent(tools):
    sql_query_agent = create_sql_agent(tools)
    
    # Debug: Print managed agents being created
    print("\n🔧 DEBUG - Creating manager agent with managed agents:")
    print(f"  - web_agent: {web_agent.name}")
    print(f"  - visual_agent: {visual_agent.name}")
    print(f"  - sql_query_agent: {sql_query_agent.name}")

    manager_agent = CodeAgent(
        tools=[],
        model=model,
        managed_agents=[web_agent, visual_agent, sql_query_agent],
        additional_authorized_imports=["time", "numpy", "pandas"],
    )

    manager_agent.prompt_templates[
        "system_prompt"
    ] = """You are a manager agent that coordinates other specialized agents to answer user questions.

    YOU HAVE ACCESS TO THESE MANAGED AGENTS:
    - web_search_agent: For web searches and retrieving online information
    - visual_agent: For creating visualizations and charts  
    - sql_query_agent_health: For querying the health database

    TO DELEGATE WORK TO MANAGED AGENTS:
    You must explicitly call them in your Python code like this:
    ```python
    # Example of delegating to the SQL agent:
    sql_result = sql_query_agent_health("Query the database for heart rate data")
    
    # Example of delegating to the web agent:
    web_result = web_search_agent("Search for normal heart rate ranges")
    
    # Example of delegating to the visual agent:
    visual_result = visual_agent("Create a chart showing heart rate over time using this data: " + str(data))
    ```

    IMPORTANT RULES:
    1. ALWAYS delegate database queries to sql_query_agent_health
    2. ALWAYS delegate web searches to web_search_agent
    3. ALWAYS delegate visualization creation to visual_agent
    4. DO NOT try to perform these tasks yourself - use the specialized agents
    5. Combine results from multiple agents to provide comprehensive answers
    6. NEVER create synthetic data or make up information
    7. Always format code blocks properly with ```python

    Pass all relevant context and instructions to the managed agents when delegating.
    """
    return manager_agent


if __name__ == "__main__":
    with MCPClient(SERVER_PARAMETERS) as tools:
        manager_agent = create_main_agent(tools)

        answer = manager_agent.run("""How is my heart health?""")
        print(answer)
