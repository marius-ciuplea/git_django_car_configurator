import sqlite3
from pydantic import BaseModel
from typing import Dict, Any, List

# --- STEP 1: DEFINE THE PYDANTIC OUTPUT MODEL ---
class SqlReadResult(BaseModel):
    """Structured response model for SELECT operations."""
    human_response: str
    raw_data: List[Dict[str, Any]]
    status: str = "SUCCESS"

# --- STEP 2: HELPER FUNCTION FOR ROBUST FALLBACK ---
def get_value(data_row: Dict[str, Any], keys: List[str]) -> Any | None:
    """Extracts the first non-None value found from a list of prioritized keys."""
    for key in keys:
        # Use .get() to safely access dictionary keys without raising KeyError
        value = data_row.get(key) 
        # Check if the value is not None (allows 0, False, empty strings, etc.)
        if value is not None:
            return value
    return None

# --- STEP 3: MAIN TOOL FUNCTION (UPDATED) ---
def execute_sql_query_select(context: Dict[str, Any]) -> SqlReadResult:
    """
    Executes a SELECT SQL query, extracts all relevant configuration details, 
    and returns them in a structured Pydantic object.
    
    Now iterates through all results to list multiple options clearly.
    """
    sql_query = context.get('sql_query')
    params = context.get('params', [])
    
    if not sql_query or not sql_query.strip().upper().startswith("SELECT"):
        return SqlReadResult(
            human_response="The provided query is invalid or not a SELECT statement. I only handle searches.",
            raw_data=[],
            status="INVALID_QUERY"
        )

    try:
        # Connect to the database
        with sqlite3.connect("db.sqlite3") as conn: 
            conn.row_factory = sqlite3.Row  # Set row_factory to get column names (keys)
            cursor = conn.cursor()
            cursor.execute(sql_query, params)
            result = cursor.fetchall()
            
            # Convert results to a list of dictionaries
            raw_dicts = [dict(row) for row in result]
            
            if not raw_dicts:
                return SqlReadResult(
                    human_response="I found no data matching your request. Maybe try a different search?",
                    raw_data=[],
                    status="NO_DATA_FOUND"
                )
            
            # --- Data Extraction and Mapping ---
            
            # MAPPING: Define the keys (in order of preference/fallbacks) based on your Django models
            NAME_MAPPING = {
                "model_name": ['model_name', 'car_model_name', 'name'], 
                "color_name": ['color_name'], 
                "engine_name": ['engine_name', 'engine_model'], 
                "wheel_style": ['wheel_style', 'style', 'wheel_type'], 
            }

            VALUE_MAPPING = {
                "engine_type": ['types', 'engine_type'],
                "engine_power": ['power', 'engine_power', 'hp'],
                "wheel_size": ['size', 'wheel_size', 'diameter'], 
                "company_name": ['company_name', 'manufacturer'], 
                "base_price": ['base_price', 'price'] 
            }
            
            all_mappings = {**NAME_MAPPING, **VALUE_MAPPING}
            
            # Use the details from the first row for a general introduction
            first_row = raw_dicts[0]
            intro_details = {}
            for key_en, key_list in all_mappings.items():
                value = get_value(first_row, key_list)
                if value is not None:
                    intro_details[key_en] = value

            # --- Construct the Summary (HUMAN_RESPONSE) ---
            
            company = intro_details.get("company_name", "the requested")
            model_name = intro_details.get("model_name", "configuration")

            # 1. Introduction
            human_summary = f"I found **{len(raw_dicts)} options** for the **{company} {model_name}**:"
            
            # 2. Iterate and detail EACH option
            option_list = []
            
            for i, data_row in enumerate(raw_dicts):
                # Extract details for the current row
                human_details = {}
                for key_en, key_list in all_mappings.items():
                    value = get_value(data_row, key_list)
                    if value is not None:
                        human_details[key_en] = value
                        
                # Build a description for this specific row
                segments = []
                
                # Wheel Details
                wheel_style = human_details.get("wheel_style")
                wheel_size = human_details.get("wheel_size")
                if wheel_style and wheel_size:
                    segments.append(f"**{wheel_size}\" {wheel_style}** wheels")
                elif wheel_style:
                    segments.append(f"**{wheel_style}** wheels")
                
                # Engine Details
                motor_name = human_details.get("engine_name")
                motor_power = human_details.get("engine_power")
                if motor_name or motor_power:
                    engine_str = ""
                    if motor_name:
                        engine_str += f"with engine **{motor_name}**"
                    if motor_power:
                        engine_str += f" ({motor_power} HP)"
                    if engine_str:
                        segments.append(engine_str)

                # Color
                color = human_details.get("color_name")
                if color:
                    segments.append(f"in **{color}**")

                # Price (Append price last, if available)
                base_price = human_details.get("base_price")
                price_str = ""
                if base_price is not None:
                    # Format price as currency (simple example)
                    price_str = f", priced at **${base_price}**"

                # Combine segments for this option
                if segments:
                    # Starts with index and lists segments joined by a comma, then adds price.
                    option_description = f"{i+1}. " + ", ".join(segments) + price_str
                    option_list.append(option_description)
            
            # 3. Join the list of options
            human_summary += "\n\n" + "\n".join(option_list) + "."
            
            # 4. Closing Message
            human_summary += "\n\nWhich one are you interested in, or would you like to save one of these configurations?"

            # 5. Return the Pydantic object
            return SqlReadResult(
                human_response=human_summary,
                raw_data=raw_dicts,
                status="SUCCESS"
            )
        
    except sqlite3.Error as e:
        return SqlReadResult(
            human_response=f"A database error occurred during the search: {e}. Please check the query and parameters.",
            raw_data=[],
            status="DB_ERROR"
        )
    except Exception as e:
        return SqlReadResult(
            human_response=f"An unexpected error occurred. Please try again. Error details: {e}",
            raw_data=[],
            status="UNEXPECTED_ERROR"
        )