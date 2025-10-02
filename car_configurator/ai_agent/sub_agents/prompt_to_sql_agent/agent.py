from google.adk.agents import LlmAgent
from ai_agent.sub_agents.prompt_to_sql_agent.prompt import PROMPT_TO_SQL_INSTRUCTIONS
# 💥 CORECȚIE: Schimbăm importul pentru a reflecta numele corect al funcției Tool.
# Presupunem că funcția ta din acel fișier este execute_sql_query_select.
from ai_agent.tools.execute_queries import execute_sql_query_select


prompt_to_sql_agent = LlmAgent(
    name="prompt_to_sql_agent",
    model="gemini-2.5-flash",
    description="A helpful agent that can generate SQL queries from user prompts and execute them using the structured SELECT tool.",
    instruction=PROMPT_TO_SQL_INSTRUCTIONS,
    # 💥 CORECȚIE: Folosim numele corect al funcției Tool.
    tools=[execute_sql_query_select],
)

# Export the agent instance
__all__ = ["prompt_to_sql_agent"]