"""
Mini SQL Agent with Agentic System (Task 4)

This module implements a complete agentic Text-to-SQL system with:
1. Query decomposition (Task 2)
2. SQL generation (Task 3)
3. Query execution with retry logic
4. Error handling and self-correction
5. Natural language result summarization
6. Comprehensive logging
"""

import time
import json
from typing import Dict, Any, Optional
from app.sql_generator import generate_sql
from app.validator import validate_sql
from app.executer import run_sql
from app.summarize import summarize_answer
from app.decompose import decompose_query
from app.llm import llm as groq_llm
from app.logger import setup_logger

logger = setup_logger(__name__)

MAX_RETRIES = 3
EXECUTION_TIMEOUT = 30  # seconds


def run_agent(user_query: str) -> Dict[str, Any]:
    """
    Main agent function that orchestrates the complete Text-to-SQL pipeline.

    Pipeline Flow:
    1. Query Understanding (Decomposition)
    2. SQL Generation
    3. Query Validation (Safety checks)
    4. Query Execution
    5. Error Handling & Retry Logic (max 3 attempts)
    6. Result Summarization

    Args:
        user_query: Natural language question

    Returns:
        Dictionary containing:
        - question: Original question
        - sql: Generated SQL query
        - result: Query execution result
        - summary: Natural language summary
        - status: success/failed/blocked/etc
        - attempts: Number of attempts made
        - execution_time_ms: Time taken to execute
        - error: Error message if any
    """

    start_time = time.time()
    attempt = 0
    last_error = None
    generated_sql = None

    logger.info("=" * 80)
    logger.info(f"STARTING NEW AGENT EXECUTION")
    logger.info(f"Question: {user_query}")
    logger.info("=" * 80)

    # STEP 1: Query Decomposition (Task 2)
    try:
        logger.info("STEP 1: Decomposing query...")
        decomposition = decompose_query(user_query)
        logger.info(f"Decomposition successful:\n{decomposition}")
    except Exception as e:
        logger.warning(f"Decomposition failed: {str(e)}")
        decomposition = None

    # STEP 2-5: SQL Generation, Validation, Execution with Retries
    while attempt < MAX_RETRIES:
        attempt += 1
        logger.info(f"\n{'=' * 60}")
        logger.info(f"ATTEMPT {attempt}/{MAX_RETRIES}")
        logger.info(f"{'=' * 60}")

        try:
            # STEP 2: SQL Generation
            logger.info("STEP 2: Generating SQL query...")

            if attempt == 1:
                # First attempt: use original question
                generated_sql = generate_sql(user_query)
            else:
                # Retry: provide error context with explicit instructions
                from app.schema import get_schema

                retry_prompt = f"""You are a PostgreSQL expert. The previous SQL query failed with a database error. Regenerate the correct SQL query.

CRITICAL RULES FOR PostgreSQL:
- In PostgreSQL, unquoted identifiers are converted to LOWERCASE
- If a column name has mixed case (e.g., customerNumber), you MUST quote it: "customerNumber"
- If the error hint shows the correct column name in quotes, use those quotes exactly
- Quote ALL column names to preserve their case

Database Schema:
{get_schema()}

Original Question: {user_query}

Previous Query Error:
{last_error}

Instructions:
1. Look at the error hint - it shows the correct column names and how to quote them
2. Use quoted column names for ALL identifiers with mixed case
3. Quote table aliases if needed
4. Verify the exact column names from the schema
5. Ensure all JOINs use quoted names consistently

Generate ONLY the corrected SQL query, nothing else:"""

                generated_sql = groq_llm.invoke(retry_prompt).content.strip()

                # Clean up markdown if present
                if generated_sql.startswith("```"):
                    generated_sql = generated_sql.split("```")[1]
                    if generated_sql.startswith("sql"):
                        generated_sql = generated_sql[3:]

                generated_sql = generated_sql.strip()

            logger.info(f"Generated SQL: {generated_sql}")

            # Check for invalid query markers
            if not generated_sql or "INVALID_QUERY" in generated_sql.upper():
                error_msg = generated_sql if generated_sql else "Empty query generated"
                logger.warning(f"Invalid query marker detected: {error_msg}")

                if attempt < MAX_RETRIES:
                    last_error = error_msg
                    continue
                else:
                    execution_time = (time.time() - start_time) * 1000
                    return {
                        "question": user_query,
                        "sql": None,
                        "result": None,
                        "summary": None,
                        "status": "failed",
                        "attempts": attempt,
                        "execution_time_ms": execution_time,
                        "error": error_msg,
                    }

            # STEP 3: Query Validation (Safety checks)
            logger.info("STEP 3: Validating SQL query...")
            is_valid = validate_sql(generated_sql)

            if not is_valid:
                error_msg = "Blocked unsafe SQL (DELETE/DROP/UPDATE/INSERT)"
                logger.error(error_msg)
                execution_time = (time.time() - start_time) * 1000

                return {
                    "question": user_query,
                    "sql": generated_sql,
                    "result": None,
                    "summary": None,
                    "status": "blocked",
                    "attempts": attempt,
                    "execution_time_ms": execution_time,
                    "error": error_msg,
                }

            logger.info("Query validation passed")

            # STEP 4: Query Execution
            logger.info("STEP 4: Executing SQL query...")
            execution_start = time.time()
            executed_output = run_sql(generated_sql)
            execution_duration = (time.time() - execution_start) * 1000

            logger.info(f"Query executed successfully in {execution_duration:.2f}ms")
            logger.info(
                f"Result rows: {len(executed_output) if executed_output else 0}"
            )

            # STEP 5: Result Summarization
            logger.info("STEP 5: Summarizing results...")
            try:
                summarized_output = summarize_answer(user_query, executed_output)
                logger.info(f"Summary: {summarized_output}")
            except Exception as e:
                logger.warning(f"Summarization failed: {str(e)}, using raw result")
                summarized_output = f"Query returned {len(executed_output) if executed_output else 0} rows"

            # SUCCESS
            execution_time = (time.time() - start_time) * 1000

            logger.info("\n" + "=" * 80)
            logger.info(f"[SUCCESS] AGENT EXECUTION SUCCESSFUL (Attempt {attempt})")
            logger.info(f"Total time: {execution_time:.2f}ms")
            logger.info("=" * 80)

            return {
                "question": user_query,
                "sql": generated_sql,
                "result": executed_output if executed_output else [],
                "summary": summarized_output,
                "status": "success" if attempt == 1 else f"success_after_retry",
                "attempts": attempt,
                "execution_time_ms": execution_time,
                "error": None,
            }

        except Exception as e:
            last_error = str(e)
            logger.error(f"Attempt {attempt} failed with error: {last_error}")

            if attempt >= MAX_RETRIES:
                # All retries exhausted
                execution_time = (time.time() - start_time) * 1000

                logger.error("\n" + "=" * 80)
                logger.error(
                    f"[FAILED] AGENT EXECUTION FAILED (After {attempt} attempts)"
                )
                logger.error(f"Final error: {last_error}")
                logger.error("=" * 80)

                return {
                    "question": user_query,
                    "sql": generated_sql,
                    "result": None,
                    "summary": None,
                    "status": "failed",
                    "attempts": attempt,
                    "execution_time_ms": execution_time,
                    "error": last_error,
                }

    # Fallback (should not reach here)
    execution_time = (time.time() - start_time) * 1000
    return {
        "question": user_query,
        "sql": generated_sql,
        "result": None,
        "summary": None,
        "status": "failed",
        "attempts": attempt,
        "execution_time_ms": execution_time,
        "error": "Unknown error",
    }
