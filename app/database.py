"""
Database Connection Management

Handles PostgreSQL database connections for query execution.
Uses SQLAlchemy and LangChain for database operations.
"""

from langchain_community.utilities import SQLDatabase
from app.config import DATABASE_URL
from app.logger import setup_logger

logger = setup_logger(__name__)

try:
    # Initialize database connection
    db = SQLDatabase.from_uri(DATABASE_URL)
    logger.info("Database connection established successfully")
except Exception as e:
    logger.error(f"Failed to connect to database: {str(e)}")
    raise Exception(f"Database connection failed: {str(e)}")
