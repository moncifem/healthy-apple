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

    manager_agent = CodeAgent(
        tools=[],
        model=model,
        managed_agents=[web_agent, visual_agent, sql_query_agent],
        additional_authorized_imports=["time", "numpy", "pandas"],
    )

    manager_agent.prompt_templates[
        "system_prompt"
    ] = """You are a manager agent. Your job is to manage the other agents and make sure they are working together to answer the user's question.
    You are also responsible for the final output of the conversation.

    IT IS CRITICAL to NEVER create synthetic data or make up informations.
    IT IS CRITICAL to always return correct code blobs as in:
    ```py
    ...
    ```

    Pass through CRITICAL informations to any sub-agent.
    """
    return manager_agent


if __name__ == "__main__":
    with MCPClient(SERVER_PARAMETERS) as tools:
        manager_agent = create_main_agent(tools)

        answer = manager_agent.run("""How is my heart health?""")
        print(answer)
