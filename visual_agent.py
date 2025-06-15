import os
from smolagents import CodeAgent, LiteLLMModel, tool

VISUAL_SYSTEM_PROMPT_PATH = os.path.join(
    os.path.dirname(__file__), "system_info", "visual_prompt.txt"
)

model = LiteLLMModel(model_id="anthropic/claude-sonnet-4-20250514", temperature=0.2)


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
