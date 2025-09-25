from google.adk.agents import LlmAgent
from ai_agent.sub_agents.prompt_to_sql_agent.prompt import PROMPT_TO_SQL_INSTRUCTIONS
from ai_agent.tools.execute_queries import execute_sql_query


prompt_to_sql_agent = LlmAgent(
    name="prompt_to_sql_agent",
    model="gemini-2.5-flash",
    description="A helpful agent that can generate SQL queries from user prompts",
    instruction=PROMPT_TO_SQL_INSTRUCTIONS,
    tools=[execute_sql_query],
    output_key="query_response"
)
