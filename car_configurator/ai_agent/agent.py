from google.adk.agents import LlmAgent
from ai_agent.prompt import ROOT_INSTRUCTIONS
from ai_agent.sub_agents.prompt_to_sql_agent.agent import prompt_to_sql_agent


root_agent = LlmAgent(
    name="ai_agent",
    model="gemini-2.5-flash",
    description="The root agent who delegates tasks to sub_agents ",
    instruction=ROOT_INSTRUCTIONS,
    sub_agents=[prompt_to_sql_agent],
)
