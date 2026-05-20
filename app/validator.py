"""
SQL Query Validator

Performs safety checks to prevent malicious queries
"""

import re
from app.logger import setup_logger

logger = setup_logger(__name__)

# Forbidden SQL operations (write operations only)
FORBIDDEN_KEYWORDS = [
    "DELETE",
    "DROP",
    "UPDATE",
    "INSERT",
    "TRUNCATE",
    "ALTER",
    "CREATE",
    "REPLACE",
]

# SQL injection patterns to block
DANGEROUS_PATTERNS = [
    r";\s*(?:DELETE|DROP|UPDATE|INSERT|TRUNCATE|ALTER|CREATE)",  # Multiple statements with write operations
    r"--\s*",  # SQL comments (can be used to hide commands)
    r"/\*.*\*/",  # Block comments
]


def validate_sql(sql: str) -> bool:
    """
    Validate SQL query for safety.

    Checks:
    1. No forbidden write operations (DELETE, DROP, UPDATE, INSERT, etc.)
    2. No SQL injection patterns
    3. Must be a SELECT query

    Args:
        sql: SQL query string

    Returns:
        True if valid, False if invalid
    """

    if not sql:
        logger.warning("Empty SQL query")
        return False

    sql_upper = sql.upper().strip()

    # Must start with SELECT
    if not sql_upper.startswith("SELECT"):
        logger.warning("Query does not start with SELECT")
        return False

    # Check for forbidden keywords using word boundaries
    # This prevents false positives from table/column names
    for keyword in FORBIDDEN_KEYWORDS:
        # Use word boundary regex to match complete keywords only
        pattern = r"\b" + keyword + r"\b"
        if re.search(pattern, sql_upper):
            logger.warning(f"Forbidden keyword '{keyword}' detected in query")
            return False

    # Check for dangerous patterns (SQL injection)
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, sql):
            logger.warning(f"Dangerous pattern detected: {pattern}")
            return False

    logger.debug("Query validation passed")
    return True


def validate_and_log(sql: str) -> tuple[bool, str]:
    """
    Validate SQL and return detailed reason if invalid.

    Returns:
        Tuple of (is_valid, reason)
    """
    if not sql:
        return False, "Empty SQL query"

    sql_upper = sql.upper().strip()

    if not sql_upper.startswith("SELECT"):
        return False, "Query must be a SELECT statement"

    for keyword in FORBIDDEN_KEYWORDS:
        pattern = r"\b" + keyword + r"\b"
        if re.search(pattern, sql_upper):
            return False, f"Forbidden keyword '{keyword}' detected"

    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, sql):
            return False, f"Dangerous pattern detected: {pattern}"

    return True, "Valid query"
