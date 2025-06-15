from smolagents import CodeAgent, InferenceClientModel
from smolagents import LiteLLMModel

# Initialize with default tools (requires smolagents[toolkit])
model = LiteLLMModel(model_id="anthropic/claude-3-5-sonnet-latest", temperature=0.2)
agent = CodeAgent(
    tools=[],  # Empty list since we'll use default tools
    model=model,
    add_base_tools=True  # This adds web search and other default tools
)

# Now the agent can search the web!
result = agent.run("What is the current weather in Paris?")
print(result)