from smolagents import CodeAgent, LiteLLMModel, MCPClient
from mcp import StdioServerParameters
import os
from dotenv import load_dotenv

load_dotenv()

model = LiteLLMModel(model_id="anthropic/claude-sonnet-4-20250514", temperature=0.2)

SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "system_info", "models.py")


def load_schema():
    with open(SCHEMA_PATH, "r") as file:
        schema = file.read()
    return schema


def get_schema_description():
    schema = load_schema()
    return f"""
    Allows you to perform SQL queries on the database. Returns a string representation of the result.
    
    The schema of the database is as follows:
    {schema}
    """


HF_TOKEN = os.getenv("HF_TOKEN")

SERVER_PARAMETERS = StdioServerParameters(
    command="npx",  # Using uvx ensures dependencies are available
    args=[
        "-y",
        "mcp-remote@latest",
        "https://grlll-health-data-real-mcp.hf.space/gradio_api/mcp/sse",
        "--transport",
        "sse-only",
        "--header",
        f"Authorization: Bearer {HF_TOKEN}",
    ],
    env={**os.environ},
)


def create_sql_agent(tools):
    agent = CodeAgent(
        tools=tools,
        model=model,
        name="sql_query_agent_health",
        description="A SQL query agent that can query the database with comprehensive personal health data.",
    )
    agent.prompt_templates["system_prompt"] = get_schema_description()
    return agent


if __name__ == "__main__":
    with MCPClient(SERVER_PARAMETERS) as tools:
        agent = create_sql_agent(tools)

        result = agent.run("What is my heart health?")
        print(result)
