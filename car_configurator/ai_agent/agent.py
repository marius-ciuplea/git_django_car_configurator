import os
import django
from google.adk.agents import LlmAgent

# =======================================================
# 💥 CRITICAL FIX: INITIALIZE DJANGO ENVIRONMENT FIRST 💥
# =======================================================

# 1. Set the environment variable for your settings file
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_configurator.settings')

# 2. Initialize Django
django.setup()

# =======================================================
# Now it's safe to import Django-dependent agents and tools
# =======================================================

from ai_agent.prompt import ROOT_INSTRUCTIONS
from ai_agent.sub_agents.prompt_to_sql_agent.agent import prompt_to_sql_agent
# 💥 REMOVED: from ai_agent.sub_agents.save_config_agent.agent import save_config_agent 💥
# Nu mai este folosit, deci nu îl importăm

# =======================================================
# 💡 ROOT AGENT DEFINITION (SIMPLIFIED) 💡
# =======================================================

root_agent = LlmAgent(
    name="ai_agent",
    model="gemini-2.5-flash",
    description="The root agent who delegates car configuration and search tasks to the Prompt-to-SQL Subagent.",
    instruction=ROOT_INSTRUCTIONS,
    # ONLY include the necessary subagent
    sub_agents=[prompt_to_sql_agent], 
)


# =======================================================
# 💥 AGENT RUNNER FUNCTION 💥
# =======================================================

async def run_agent_process(prompt: str, tool_context: dict) -> list:
    """
    Asynchronous function that runs the root agent, consumes the event generator,
    and returns a list of events.
    """
    global root_agent
    
    events_list = []
    
    # Run the agent. The tool_context (containing user/session data)
    # will be managed by the underlying framework when tools are called.
    agent_generator = root_agent.run_async(prompt)
    
    # 2. Consume the asynchronous generator
    async for event in agent_generator:
        # Appending all events for synchronous processing
        events_list.append(event)
        
    return events_list

# Export the agent instance and runner function
__all__ = ["root_agent", "run_agent_process"]