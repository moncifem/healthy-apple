from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    WebSearchTool,
    MCPClient,
    LiteLLMModel,
)
from tool import visit_webpage
import os
from sql_agent import create_sql_agent, SERVER_PARAMETERS

VISUAL_SYSTEM_PROMPT_PATH = os.path.join(
    os.path.dirname(__file__), "system_info", "visual_prompt.txt"
)

model = LiteLLMModel(model_id="anthropic/claude-sonnet-4-20250514", temperature=0.2)

web_agent = ToolCallingAgent(
    tools=[WebSearchTool(), visit_webpage],
    model=model,
    max_steps=1,
    name="web_search_agent",
    description="Runs web searches for you.",
)

# Create a custom system prompt for the visual agent
custom_visual_prompt = open(VISUAL_SYSTEM_PROMPT_PATH).read()

visual_agent = CodeAgent(
    tools=[],
    model=model,
    additional_authorized_imports=[
        "matplotlib",
        "matplotlib.pyplot",
        "seaborn",
        "plotly",
        "plotly.graph_objects",
        "plotly.express",
        "plotly.offline",
        "numpy",
        "pandas",
        "scipy",
        "datetime",
        "math",
        "random",
    ],
    name="visual_agent",
    description="Creates beautiful, professional visualizations and saves them locally. Always uses proper code format and saves files correctly.",
)

# Modify the system prompt after initialization
visual_agent.prompt_templates["system_prompt"] = custom_visual_prompt


def create_main_agent(tools):
    sql_query_agent = create_sql_agent(tools)

    manager_agent = CodeAgent(
        tools=[],
        model=model,
        managed_agents=[web_agent, visual_agent, sql_query_agent],
        additional_authorized_imports=["time", "numpy", "pandas"],
    )
    return manager_agent


if __name__ == "__main__":
    with MCPClient(SERVER_PARAMETERS) as tools:
        manager_agent = create_main_agent(tools)

        answer = manager_agent.run("""How is my heart health?""")
        print(answer)
