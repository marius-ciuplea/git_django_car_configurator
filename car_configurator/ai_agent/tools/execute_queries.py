import sqlite3

def execute_sql_query(sql_query: str) -> dict:
    """
    Execute an SQL query and return a human-friendly result.

    Args:
        sql_query (str): The SQL query to be executed.

    Returns:
        dict: A dictionary containing the query, human-readable result, and raw data.
    """
    try:
        with sqlite3.connect("db.sqlite3") as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query)
            
            # Preluăm numele coloanelor din cursor.description
            columns = [description[0] for description in cursor.description]
            result = cursor.fetchall()

            if not result:
                return {
                    "sql_query": sql_query,
                    "human_readable": "No data found for the query.",
                    "raw_result": []
                }

            # Construim un text human-readable generic, incluzând numele coloanelor
            human_readable_text = ""
            for row in result:
                row_items = []
                for col, value in zip(columns, row):
                    row_items.append(f"{col}: {value}")
                human_readable_text += ", ".join(row_items) + "\n"
            
            return {
                "sql_query": sql_query,
                "human_readable": f"Query result:\n{human_readable_text}",
                "raw_result": result
            }

    except Exception as e:
        return {
            "sql_query": sql_query,
            "human_readable": f"There was an error executing the query: {str(e)}",
            "raw_result": None
        }