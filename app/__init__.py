"""
Text-to-SQL Agent Package

A complete AI-powered agentic system for converting natural language questions
into SQL queries, executing them, and returning results with natural language summaries.

Features:
- Automatic query decomposition
- LLM-based SQL generation
- Safe query validation
- Automatic retry logic
- Natural language summarization
- FastAPI REST API
- Comprehensive evaluation framework
- Detailed logging

Usage:
    from app.agent import run_agent
    result = run_agent("How many customers from USA?")
"""

__version__ = "1.0.0"
__author__ = "Text-to-SQL Agent System"
__all__ = [
    "agent",
    "decompose",
    "sql_generator",
    "validator",
    "executer",
    "summarize",
    "database",
    "schema",
    "llm",
    "config",
    "logger",
    "prompt",
    "evaluation",
]
