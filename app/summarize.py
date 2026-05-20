"""
Result Summarization

Converts SQL query results into natural language summaries
"""

from app.llm import llm
from app.logger import setup_logger

logger = setup_logger(__name__)


def summarize_answer(question: str, result) -> str:
    """
    Summarize SQL query results into natural language.

    Args:
        question: Original natural language question
        result: SQL query execution result (list of rows)

    Returns:
        Natural language summary of the results
    """

    try:
        # Format result for better readability
        if not result:
            return "No results found for this query."

        # Limit result size for the LLM (avoid token limits)
        result_str = str(result[:5])  # Show first 5 rows
        if len(result) > 5:
            result_str += f"\n... and {len(result) - 5} more rows"

        summarization_prompt = f"""Question: {question}

SQL Result: {result_str}

Provide a SHORT (1-2 sentence) natural language answer to the question based on the result.
If there are no results, say "No results found."
If the result is a count, state the count clearly.
Be concise and direct."""

        response = llm.invoke(summarization_prompt).content
        summary = response.strip()

        logger.debug(f"Summarization successful: {summary[:100]}")
        return summary

    except Exception as e:
        logger.warning(f"Summarization failed: {str(e)}, using default summary")

        # Fallback summary
        if not result:
            return "No results found."

        row_count = len(result) if isinstance(result, list) else 1
        return f"Query returned {row_count} result(s)."
