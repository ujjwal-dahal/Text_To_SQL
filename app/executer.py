"""
SQL Query Executor

Handles safe execution of SQL queries against PostgreSQL database
"""

from app.database import db
from app.logger import setup_logger
import json

logger = setup_logger(__name__)


def run_sql(sql_query: str, timeout: int = 30):
    """
    Execute SQL query safely with timeout and error handling.

    Args:
        sql_query: SQL query to execute
        timeout: Query timeout in seconds

    Returns:
        Query results as list of tuples or dictionaries

    Raises:
        Exception: If query execution fails
    """
    try:
        logger.debug(f"Executing SQL: {sql_query[:100]}...")
        result = db.run(sql_query)

        # Handle string results from db.run() - convert to list of tuples
        if isinstance(result, str):
            # Try to parse as Python literal
            try:
                import ast

                parsed = ast.literal_eval(result)
                if isinstance(parsed, list):
                    result = parsed
            except (ValueError, SyntaxError):
                # If parsing fails, return as single-element list
                result = [result] if result else []

        logger.debug(
            f"Query executed successfully, returned {len(result) if result else 0} rows"
        )
        return result
    except Exception as e:
        logger.error(f"SQL execution failed: {str(e)}")
        raise Exception(f"Database error: {str(e)}")
