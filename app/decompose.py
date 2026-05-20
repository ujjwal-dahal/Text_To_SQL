"""
Query Understanding and Decomposition (Task 2)

Breaks down natural language questions into structured components:
- Intent: What is being asked
- Tables: Which tables are involved
- Columns: Which columns are needed
- Filters: Any WHERE conditions
- Joins: Any JOINs required
"""

from typing import Dict, List, Optional
from app.llm import llm
from app.logger import setup_logger

logger = setup_logger(__name__)


class QueryDecomposition:
    """
    Represents a decomposed SQL query structure
    """

    def __init__(
        self,
        question: str,
        intent: str,
        tables: List[str],
        columns: List[str],
        filters: Optional[List[str]] = None,
        joins: Optional[List[str]] = None,
        aggregations: Optional[List[str]] = None,
    ):
        self.question = question
        self.intent = intent
        self.tables = tables if tables else []
        self.columns = columns if columns else []
        self.filters = filters if filters else []
        self.joins = joins if joins else []
        self.aggregations = aggregations if aggregations else []

    def to_dict(self) -> Dict:
        """Convert decomposition to dictionary"""
        return {
            "question": self.question,
            "intent": self.intent,
            "tables": self.tables,
            "columns": self.columns,
            "filters": self.filters,
            "joins": self.joins,
            "aggregations": self.aggregations,
        }

    def __str__(self) -> str:
        return f"""
Query Decomposition:
  Intent: {self.intent}
  Tables: {', '.join(self.tables)}
  Columns: {', '.join(self.columns)}
  Filters: {self.filters if self.filters else 'None'}
  Joins: {self.joins if self.joins else 'None'}
  Aggregations: {self.aggregations if self.aggregations else 'None'}
"""


def decompose_query(question: str) -> QueryDecomposition:
    """
    Decompose a natural language question into structured components.
    Uses LLM-based decomposition for better accuracy.

    Args:
        question: Natural language question

    Returns:
        QueryDecomposition object with extracted components
    """

    decomposition_prompt = f"""Analyze this SQL question and extract its components in JSON format.

Question: {question}

Return ONLY valid JSON (no markdown, no extra text) with this exact structure:
{{
    "intent": "what is being asked (e.g., 'Count total customers', 'Retrieve orders')",
    "tables": ["list", "of", "involved", "tables"],
    "columns": ["list", "of", "needed", "columns"],
    "filters": ["list of WHERE conditions if any"],
    "joins": ["list of JOIN conditions if any"],
    "aggregations": ["list of aggregation functions like COUNT, SUM if any"]
}}

Example:
Question: "How many customers are from the USA?"
Answer:
{{
    "intent": "Count total customers by country",
    "tables": ["customers"],
    "columns": ["customerNumber"],
    "filters": ["country = 'USA'"],
    "joins": [],
    "aggregations": ["COUNT(*)"]
}}
"""

    try:
        response = llm.invoke(decomposition_prompt).content

        # Parse JSON response
        import json

        decomp_data = json.loads(response)

        decomposition = QueryDecomposition(
            question=question,
            intent=decomp_data.get("intent", ""),
            tables=decomp_data.get("tables", []),
            columns=decomp_data.get("columns", []),
            filters=decomp_data.get("filters", []),
            joins=decomp_data.get("joins", []),
            aggregations=decomp_data.get("aggregations", []),
        )

        logger.info(f"Query decomposed successfully:\n{decomposition}")
        return decomposition

    except Exception as e:
        logger.warning(f"LLM-based decomposition failed: {str(e)}, using fallback")
        # Fallback: simple rule-based decomposition
        return _fallback_decompose(question)


def _fallback_decompose(question: str) -> QueryDecomposition:
    """
    Fallback rule-based decomposition when LLM fails
    """
    question_lower = question.lower()

    # Detect intent
    if "count" in question_lower or "how many" in question_lower:
        intent = "Count/Count rows"
    elif "sum" in question_lower or "total" in question_lower:
        intent = "Sum/Calculate total"
    elif "average" in question_lower or "avg" in question_lower:
        intent = "Average calculation"
    elif "max" in question_lower or "maximum" in question_lower:
        intent = "Find maximum"
    elif "min" in question_lower or "minimum" in question_lower:
        intent = "Find minimum"
    elif (
        "list" in question_lower or "show" in question_lower or "get" in question_lower
    ):
        intent = "Retrieve/List data"
    else:
        intent = "Retrieve data"

    # Simple table detection (based on keywords)
    tables = []
    table_keywords = {
        "customer": "customers",
        "order": "orders",
        "product": "products",
        "payment": "payments",
        "employee": "employees",
        "office": "offices",
    }

    for keyword, table in table_keywords.items():
        if keyword in question_lower:
            tables.append(table)

    if not tables:
        tables = ["customers"]  # default

    # Extract filters (very basic)
    filters = []
    if " from " in question_lower:
        parts = question_lower.split(" from ")
        if len(parts) > 1:
            filters.append(parts[1].split()[0] if parts[1].split() else "")

    columns = ["*"]  # Default to all columns

    decomposition = QueryDecomposition(
        question=question,
        intent=intent,
        tables=tables,
        columns=columns,
        filters=filters,
    )

    logger.info(f"Fallback decomposition used:\n{decomposition}")
    return decomposition
