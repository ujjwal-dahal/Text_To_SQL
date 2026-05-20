"""
Database Schema Information

Retrieves and caches database schema for use in SQL generation.
"""

from app.database import db
import re
from app.logger import setup_logger

logger = setup_logger(__name__)

# Cache schema to avoid repeated database calls
_schema_cache = None


def get_schema() -> str:
    """
    Get database schema information.

    Retrieves table definitions including columns, data types,
    and relationships. Cleans up unnecessary comments.

    Returns:
        Formatted schema string
    """
    global _schema_cache

    # Return cached schema if available
    if _schema_cache:
        return _schema_cache

    try:
        # Get raw schema from database
        raw_schema = db.get_table_info()

        # Remove SQL comments (/* ... */)
        clean_schema = re.sub(r"/\*.*?\*/", "", raw_schema, flags=re.DOTALL)

        # Remove extra whitespace
        clean_schema = re.sub(r"\n\s*\n", "\n", clean_schema)

        _schema_cache = clean_schema
        logger.info("Schema loaded successfully")
        return clean_schema

    except Exception as e:
        logger.error(f"Failed to retrieve schema: {str(e)}")
        return ""


def clear_schema_cache():
    """Clear the schema cache to force refresh on next call"""
    global _schema_cache
    _schema_cache = None
    logger.info("Schema cache cleared")


def print_schema():
    """Print schema for debugging purposes"""
    schema = get_schema()
    print(schema)
