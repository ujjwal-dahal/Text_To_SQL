"""
SQL Query Generator (Task 3)

Converts natural language questions to SQL queries using LLM with few-shot prompting.
"""

from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate

from app.schema import get_schema
from app.prompt import build_prefix, EXAMPLES
from app.llm import llm as groq_llm
from app.logger import setup_logger

logger = setup_logger(__name__)


def build_few_shot_prompt():
    """Build the few-shot prompt template"""
    return FewShotPromptTemplate(
        prefix=build_prefix(get_schema()),
        examples=EXAMPLES,
        example_prompt=PromptTemplate.from_template(template=""" 
              User Input : {input} 
              SQL Query : {query}
              """),
        suffix="""
          User Input: {question}
          
          SQL Query:
          """,
        input_variables=["question"],
    )


def generate_sql(question: str) -> str:
    """
    Generate SQL query from natural language question.

    Uses few-shot prompting with examples to guide the LLM
    towards generating correct, executable SQL queries.

    Args:
        question: Natural language question

    Returns:
        Generated SQL query string

    Example:
        >>> generate_sql("How many customers from USA?")
        "SELECT COUNT(*) FROM customers WHERE country = 'USA';"
    """
    try:
        # Build the prompt
        few_shot_prompt = build_few_shot_prompt()

        # Create the chain
        sql_query_chain = few_shot_prompt | groq_llm

        # Generate SQL
        response = sql_query_chain.invoke({"question": question})
        generated_sql = response.content.strip()

        # Clean up markdown if present
        if generated_sql.startswith("```"):
            generated_sql = generated_sql.split("```")[1]
            if generated_sql.startswith("sql"):
                generated_sql = generated_sql[3:]

        generated_sql = generated_sql.strip()

        logger.debug(f"Generated SQL: {generated_sql}")
        return generated_sql

    except Exception as e:
        logger.error(f"SQL generation failed: {str(e)}")
        return f"INVALID_QUERY: {str(e)}"
