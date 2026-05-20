"""
Configuration Management

Loads environment variables for database and LLM configuration.
"""

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# LLM Configuration (Groq)
GROQ_MODEL_NAME = os.getenv("GROQ_MODEL_NAME", "mixtral-8x7b-32768")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

# Agent Configuration
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
QUERY_TIMEOUT = int(os.getenv("QUERY_TIMEOUT", "30"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
