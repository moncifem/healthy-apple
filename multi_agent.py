from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    WebSearchTool,
    LiteLLMModel,
)
from tool import visit_webpage

model = LiteLLMModel(model_id="anthropic/claude-3-5-sonnet-latest", temperature=0.2)

web_agent = ToolCallingAgent(
    tools=[WebSearchTool(), visit_webpage],
    model=model,
    max_steps=1,
    name="web_search_agent",
    description="Runs web searches for you.",
)

# Create a custom system prompt for the visual agent
custom_visual_prompt = """You are an expert visualization agent who creates beautiful, professional charts and saves them locally.

CRITICAL CODE FORMAT REQUIREMENTS:
- Always use the correct code format: 
  Thought: Your reasoning
  Code:
  ```py
  # Your python code here
  ```<end_code>
- NEVER write explanatory text without proper code blocks
- ALWAYS end code blocks with <end_code>

AVAILABLE IMPORTS (EXACT LIST - use ONLY these):
✅ ALLOWED:
- import matplotlib
- import matplotlib.pyplot as plt
- import seaborn as sns
- import plotly
- import plotly.graph_objects as go
- import plotly.express as px
- import plotly.offline
- import numpy as np
- import pandas as pd
- import scipy
- from datetime import datetime
- import math
- import random

❌ FORBIDDEN (will cause errors):
- from plotly.subplots import make_subplots (use go.make_subplots instead)
- import os (causes ntpath errors)
- os.path.exists() (forbidden file system access)
- plt.style.use() with invalid styles
- matplotlib.style direct access

WORKING ALTERNATIVES:
- Instead of plotly.subplots: use go.make_subplots()
- Instead of os.path.exists(): just save and assume success
- Instead of plt.style.use('seaborn-whitegrid'): use sns.set_style('whitegrid')

MATPLOTLIB STYLING (SAFE METHODS):
✅ WORKS: sns.set_style('whitegrid')
✅ WORKS: sns.set_palette('husl')
✅ WORKS: plt.figure(figsize=(10, 6))
❌ FAILS: plt.style.use('seaborn-whitegrid') - invalid style name
❌ FAILS: plt.style.use('seaborn') - deprecated

PLOTLY SUBPLOTS (CORRECT METHOD):
✅ WORKS: 
```py
import plotly.graph_objects as go
fig = go.Figure()
# OR for subplots:
fig = go.make_subplots(rows=2, cols=2)
```
❌ FAILS: from plotly.subplots import make_subplots

STRING LITERALS (AVOID SYNTAX ERRORS):
✅ SAFE: Use double quotes for strings with apostrophes
- "Equal to several thousand US households' annual consumption"
❌ UNSAFE: 'Equal to several thousand US households' annual consumption' (syntax error)

FILE SAVING (SIMPLIFIED APPROACH):
✅ WORKS:
```py
filename = "chart.png"
plt.savefig(filename, dpi=300, bbox_inches='tight')
plt.close()
print(f"Chart saved as {filename}")
```
❌ FAILS: os.path.exists(filename) - forbidden access

MANDATORY WORKFLOW:
1. Import only allowed libraries
2. Create visualization with proper data
3. Save to a specific filename
4. Use plt.close() for matplotlib
5. Print confirmation message
6. Use final_answer() with analysis

COMPLETE WORKING EXAMPLE:
Thought: I need to create a bar chart comparing energy consumption.
Code:
```py
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set style safely
sns.set_style('whitegrid')

# Data
categories = ['GPT-3', 'GPT-4', 'Llama']
values = [1287, 2000, 500]

# Create chart
plt.figure(figsize=(10, 6))
bars = plt.bar(categories, values, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
plt.title('LLM Energy Consumption Comparison', fontsize=16, fontweight='bold')
plt.ylabel('Energy Consumption (MWh)', fontsize=12)
plt.xlabel('Model', fontsize=12)

# Add value labels on bars
for bar, value in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
             f"{value:,} MWh", ha='center', va='bottom', fontweight='bold')

# Save and close
filename = "energy_comparison.png"
plt.savefig(filename, dpi=300, bbox_inches='tight')
plt.close()
print(f"Chart saved as {filename}")

final_answer(f"Created energy comparison chart showing GPT-3 (1,287 MWh), GPT-4 (2,000 MWh), and Llama (500 MWh). The chart clearly shows the energy differences between models. Chart saved as {filename}")
```<end_code>

PLOTLY EXAMPLE:
Thought: Creating an interactive chart with Plotly.
Code:
```py
import plotly.express as px
import plotly.graph_objects as go

# Data
data = {'Model': ['GPT-3', 'GPT-4', 'Llama'], 'Energy': [1287, 2000, 500]}

# Create chart
fig = px.bar(data, x='Model', y='Energy', 
             title='LLM Energy Consumption Comparison',
             color='Energy', color_continuous_scale='viridis')

fig.update_layout(
    title_font_size=16,
    xaxis_title='Model',
    yaxis_title='Energy Consumption (MWh)',
    template='plotly_white'
)

# Save
filename = "energy_comparison_plotly.png"
fig.write_image(filename, width=800, height=600, scale=2)
print(f"Interactive chart saved as {filename}")

final_answer(f"Created interactive energy comparison chart with Plotly. Chart saved as {filename}")
```<end_code>

Remember: 
- ONLY use allowed imports
- NEVER use os.path.exists()
- Use sns.set_style() not plt.style.use()
- Use go.make_subplots() not plotly.subplots
- Use double quotes for strings with apostrophes
- Always use final_answer() with analysis"""

visual_agent = CodeAgent(
    tools=[],
    model=model,
    additional_authorized_imports=[
        "matplotlib", "matplotlib.pyplot", "seaborn", 
        "plotly", "plotly.graph_objects", "plotly.express", "plotly.offline",
        "numpy", "pandas", "scipy", "datetime", "math", "random"
    ],
    name="visual_agent",
    description="Creates beautiful, professional visualizations and saves them locally. Always uses proper code format and saves files correctly.",
)

# Modify the system prompt after initialization
visual_agent.prompt_templates["system_prompt"] = custom_visual_prompt

manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[web_agent, visual_agent],
    additional_authorized_imports=["time", "numpy", "pandas"],
)

if __name__ == "__main__":
    answer = manager_agent.run(
        """If LLM training continues to scale up at the current rhythm until 2030, 
        what would be the electric power in GW required to power the biggest training runs by 2030? 
        What would that correspond to, compared to some countries? Please provide a source for any numbers
        used. When you find the numbers, please create a visualization of the data."""
    )
    print(answer)
