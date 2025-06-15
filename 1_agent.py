from smolagents import CodeAgent, InferenceClientModel
from smolagents import LiteLLMModel

model = LiteLLMModel(model_id="anthropic/claude-sonnet-4-20250514", temperature=0.2)


# Create an agent with no tools
agent = CodeAgent(tools=[], model=model)

# Run the agent with a task
result = agent.run("Calculate the sum of numbers from 1 to 10")
print(result)
