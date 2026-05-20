from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging
from app.agent import run_agent
from app.logger import setup_logger

# Setup logging
logger = setup_logger(__name__)

app = FastAPI(
    title="Text-to-SQL Agent API",
    description="AI-powered SQL generation and execution system",
    version="1.0.0",
)


class SQLQuestion(BaseModel):
    """Request model for SQL agent"""

    question: str


class SQLResponse(BaseModel):
    """Response model for SQL agent"""

    question: str
    sql: Optional[str]
    result: Optional[list]
    summary: Optional[str]
    status: str
    attempts: int
    execution_time_ms: float
    error: Optional[str] = None


@app.post("/agent/sql", response_model=SQLResponse)
def sql_agent(payload: SQLQuestion):
    """
    Text-to-SQL Agent Endpoint

    Process natural language questions and convert them to SQL queries.
    Features:
    - Automatic query decomposition
    - SQL generation using LLM
    - Safe query validation
    - Automatic error handling with retry logic (max 3 attempts)
    - Natural language result summarization
    - Comprehensive logging
    """
    try:
        logger.info(f"Received question: {payload.question}")

        result = run_agent(payload.question)

        logger.info(f"Agent result status: {result.get('status')}")

        return SQLResponse(**result)

    except Exception as e:
        logger.error(f"Unexpected error in agent: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Text-to-SQL Agent"}


@app.get("/schema")
def get_schema():
    """Get database schema for debugging"""
    try:
        from app.schema import get_schema as get_db_schema

        schema = get_db_schema()
        return {"status": "success", "schema": schema}
    except Exception as e:
        logger.error(f"Failed to retrieve schema: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Schema retrieval failed: {str(e)}"
        )


@app.get("/")
def root():
    """API Information"""
    return {
        "service": "Text-to-SQL Agent API",
        "version": "1.0.0",
        "endpoints": {
            "agent": "/agent/sql (POST)",
            "health": "/health (GET)",
            "schema": "/schema (GET)",
            "docs": "/docs",
        },
    }
