import os
import django
import sys
from ai_agent.agent import root_agent

# =======================================================
# 💥 CRITICAL: INITIALIZE DJANGO ENVIRONMENT 💥
# =======================================================
try:
    # 1. SETTINGS MODULE: Replace 'your_project_name.settings' with your actual path!
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_configurator.settings') 
    
    # 2. Setup Django
    django.setup()
except Exception as e:
    print(f"FATAL ERROR: Could not initialize Django. Check settings path. Error: {e}")
    sys.exit(1)
# =======================================================


# --- 1. Define the MOCK User ID ---
# Use the ID of a known, existing user in your Django database (e.g., your admin user).
MOCK_USER_ID = "11" 

# --- 2. Define the Agent Context ---
# This simulates the API successfully grabbing the user's session ID.
AGENT_CONTEXT = {
    "user_context": MOCK_USER_ID, 
}

# --- 3. Define Mock Configuration Data ---
# The Root Agent expects the *raw_dicts* output from the SQL Agent.
# You must manually construct this data, including the IDs you want to save.
# ***You must replace these ID values (1, 22, 1, 2) with actual, valid IDs from your database!***
MOCK_CONFIG_DATA = [
    {
        "car_model_id": 1, 
        "engine_id": 1, 
        "color_id": 22, 
        "wheel_id": 2
    }
]

# --- 4. Simulate the Agent Run (Bypassing the LLM) ---
# Since we know the Root Agent's job is just to call save_car_configuration,
# we can call the Save Agent's tool function directly for the fastest test.
from ai_agent.tools.save_config import save_car_configuration 

print(f"--- Starting Save Test (User ID: {MOCK_USER_ID}) ---")

try:
    # Call the save function directly with the mock data
    result = save_car_configuration(config=MOCK_CONFIG_DATA, user_context=MOCK_USER_ID)
    
    print("\n✅ SAVE TEST RESULT:")
    print(f"Status: {result.get('status')}")
    print(f"Message: {result.get('message')}")
    
except Exception as e:
    print(f"\n❌ A critical error occurred during execution: {e}")
