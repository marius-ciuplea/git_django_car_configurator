"""Agent tools"""

import sqlite3

def format_cars_human_readable(sql_result, user_context: str = "") -> str:
    """
    Transform the SQL result into friendly English text.

    Args:
        sql_result (list of tuples): ex: [("Volkswagen", "Tiguan", "40000"), ("Volkswagen", "Tuareg", "60000")]  
        user_context (str): optional context about user

    Returns:
        str: human-readable description of the cars
    """
    if not sql_result:
        return "Sorry! No cars match your criteria."

    descriptions = []
    for row in sql_result:
        if len(row) == 3:  # company, model, price
            company, model, price = row
            descriptions.append(f"{company} {model} (base price: {price} EUR)")
        elif len(row) == 2:  # company, model
            company, model = row
            descriptions.append(f"{company} {model}")
        else:
            descriptions.append(" - ".join(map(str, row)))

    response_text = "I found the following cars:\n" + "\n".join(descriptions)

    if user_context:
        response_text += f"\nPersonalized suggestion for you ({user_context})"

    return response_text


def execute_sql_query(sql_query: str, user_context: str = "") -> dict:
    """
    Execute SQL queries and return a human-friendly result in English.

    Args:
        sql_query (str): SQL query to be executed
        user_context (str, optional): context about the user, default is empty string

    Returns:
        dict: {
            "sql_query": the executed SQL query,
            "human_readable": human-friendly text in English,
            "raw_result": raw SQL result (list of tuples)
        }
    """
    try:
        with sqlite3.connect("db.sqlite3") as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchall()

            human_readable_text = format_cars_human_readable(result, user_context=user_context)

            return {
                "sql_query": sql_query,
                "human_readable": human_readable_text,
                "raw_result": result
            }

    except Exception as e:
        return {
            "sql_query": sql_query,
            "human_readable": f"There was an error executing the query: {str(e)}",
            "raw_result": None
        }
