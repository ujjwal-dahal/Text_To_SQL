# Text-to-SQL Agent System with FastAPI

A complete AI-powered agentic system that converts natural language questions into SQL queries, executes them, and returns results with natural language summaries.

## Overview

This project implements a **Text-to-SQL Agent** system that demonstrates:

1. **Task 1**: SQL Benchmark Dataset preparation and evaluation strategy design
2. **Task 2**: Query understanding through decomposition (Intent, Tables, Columns, Filters, Joins)
3. **Task 3**: Text-to-SQL pipeline with structured generation, validation, and execution
4. **Task 4**: Agentic system with FastAPI endpoint, retry logic, and self-correction

## System Architecture

```
Natural Language Question
        ↓
Step 1: Query Decomposition (Task 2)
        ├─ Intent Detection
        ├─ Table Identification
        ├─ Column Selection
        ├─ Filter Detection
        └─ Join Identification
        ↓
Step 2: SQL Generation (Task 3)
        ├─ LLM-based query generation
        ├─ Few-shot prompting with examples
        └─ Output cleaning and validation
        ↓
Step 3: Query Validation
        ├─ Safe SQL checks (block DELETE/DROP/UPDATE/INSERT)
        ├─ SQL injection prevention
        └─ Syntax verification
        ↓
Step 4: Query Execution
        └─ PostgreSQL execution with error handling
        ↓
Step 5: Error Handling & Retry Logic
        ├─ Max 3 retry attempts
        ├─ Context-aware error feedback
        └─ Self-correction mechanism
        ↓
Step 6: Result Summarization
        └─ Natural language answer generation
        ↓
Final Output (JSON Response)
```

## Features

### ✅ Core Features

- **Automatic Query Decomposition**: Breaks down natural language into structured components
- **LLM-Based SQL Generation**: Uses Groq API with few-shot prompting
- **Safe Query Validation**: Prevents malicious queries (DELETE, DROP, UPDATE, INSERT)
- **Automatic Retry Logic**: Up to 3 attempts with error-aware regeneration
- **Natural Language Summarization**: Converts SQL results to human-readable summaries
- **Comprehensive Logging**: Detailed logs for all steps
- **FastAPI Endpoint**: Production-ready REST API

### 📊 Evaluation Features

- **Benchmark Testing Framework**: Evaluate against known test cases
- **Performance Metrics**: Track success rates, execution times, retry rates
- **Detailed Reports**: JSON and CSV export of evaluation results
- **Performance Tracking**: Monitor query generation latency and accuracy

## Technology Stack

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **LLM Provider**: Groq (Mixtral-8x7b)
- **ORM**: SQLAlchemy (via LangChain)
- **Language**: Python 3.8+

## Project Structure

```
Text_To_SQL/
├── app/
│   ├── agent.py              # Main agentic system orchestrator
│   ├── decompose.py          # Query decomposition (Task 2)
│   ├── sql_generator.py      # SQL generation with LLM
│   ├── validator.py          # Query safety validation
│   ├── executer.py           # Query execution
│   ├── summarize.py          # Result summarization
│   ├── database.py           # Database connection
│   ├── schema.py             # Schema retrieval
│   ├── llm.py                # LLM initialization
│   ├── config.py             # Configuration management
│   ├── logger.py             # Logging setup
│   ├── prompt.py             # LLM prompts and examples
│   ├── evaluation.py         # Evaluation framework
│   └── main.py               # FastAPI application
├── evaluate.py               # Evaluation script
├── sql_questions.csv         # Benchmark questions
├── database_schema.txt       # Database schema definition
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL database
- Groq API key

### Setup Steps

1. **Clone/Extract the project**

```bash
cd Text_To_SQL
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/Scripts/activate  # On Windows
# or
source venv/bin/activate      # On Linux/Mac
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/database_name

# Groq LLM Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL_NAME=mixtral-8x7b-32768

# Agent Configuration (Optional)
MAX_RETRIES=3
QUERY_TIMEOUT=30
LOG_LEVEL=INFO
```

5. **Verify database connection**

```bash
python -c "from app.database import db; print('✓ Database connected')"
```

## Usage

### Starting the FastAPI Server

```bash
# Development server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production server
uvicorn app.main:app --workers 4
```

The API will be available at: `http://localhost:8000`

**Swagger Docs**: `http://localhost:8000/docs`

### Using the SQL Agent Endpoint

#### Request

```bash
curl -X POST "http://localhost:8000/agent/sql" \
  -H "Content-Type: application/json" \
  -d '{"question": "How many customers are from USA?"}'
```

Or in Python:

```python
import requests

url = "http://localhost:8000/agent/sql"
payload = {"question": "How many customers are from USA?"}

response = requests.post(url, json=payload)
result = response.json()

print(f"SQL: {result['sql']}")
print(f"Result: {result['result']}")
print(f"Summary: {result['summary']}")
print(f"Status: {result['status']}")
print(f"Attempts: {result['attempts']}")
```

#### Response

```json
{
  "question": "How many customers are from USA?",
  "sql": "SELECT COUNT(*) as customer_count FROM customers WHERE country = 'USA';",
  "result": [
    {
      "customer_count": 36
    }
  ],
  "summary": "There are 36 customers from the USA.",
  "status": "success",
  "attempts": 1,
  "execution_time_ms": 245.67,
  "error": null
}
```

### Running Evaluation

#### Step 1: Load Questions from Benchmark Dataset

```bash
python evaluate.py sql_questions.csv logs
```

This will:

1. Load all questions from `sql_questions.csv`
2. Run the agent against each question
3. Generate evaluation reports
4. Export results to JSON and CSV

#### Step 2: Check Evaluation Reports

- JSON Report: `logs/evaluation_report.json`
- CSV Results: `logs/evaluation_results.csv`
- Console Output: Detailed metrics and summary

#### Programmatic Evaluation

```python
from app.evaluation import EvaluationFramework

# Create evaluator
evaluator = EvaluationFramework()

# Evaluate questions
questions = [
    "How many customers are from USA?",
    "List all products",
    "Show orders from Germany",
]

results = evaluator.evaluate_batch(questions)

# Get metrics
metrics = evaluator.calculate_metrics()
print(f"Success Rate: {metrics['execution_success_rate']:.1f}%")

# Print report
evaluator.print_report()

# Export results
evaluator.export_json("report.json")
evaluator.export_csv("results.csv")
```

## API Endpoints

### 1. POST /agent/sql

**Text-to-SQL Agent Endpoint**

- **Input**: Natural language question
- **Output**: SQL query, execution result, natural language summary
- **Features**: Automatic retry logic, error handling, logging

**Request Body**:

```json
{
  "question": "What is your question?"
}
```

**Response Body**:

```json
{
  "question": "string",
  "sql": "string or null",
  "result": "array or null",
  "summary": "string or null",
  "status": "success|failed|blocked",
  "attempts": 1,
  "execution_time_ms": 123.45,
  "error": "null or error message"
}
```

### 2. GET /health

**Health Check**

```bash
curl http://localhost:8000/health
```

Response:

```json
{
  "status": "healthy",
  "service": "Text-to-SQL Agent"
}
```

### 3. GET /

**API Information**

```bash
curl http://localhost:8000/
```

Response:

```json
{
  "service": "Text-to-SQL Agent API",
  "version": "1.0.0",
  "endpoints": {
    "agent": "/agent/sql (POST)",
    "health": "/health (GET)",
    "docs": "/docs"
  }
}
```

## Configuration

### Environment Variables

| Variable          | Default              | Description                  |
| ----------------- | -------------------- | ---------------------------- |
| `DATABASE_URL`    | Required             | PostgreSQL connection string |
| `GROQ_API_KEY`    | Required             | Groq API key for LLM         |
| `GROQ_MODEL_NAME` | `mixtral-8x7b-32768` | LLM model to use             |
| `MAX_RETRIES`     | `3`                  | Maximum retry attempts       |
| `QUERY_TIMEOUT`   | `30`                 | Query timeout in seconds     |
| `LOG_LEVEL`       | `INFO`               | Logging level                |

### Logging Configuration

Logs are stored in the `logs/` directory with:

- Daily log files: `agent_YYYYMMDD.log`
- Console output for important events
- Detailed timestamps and function names
- Full error traces for debugging

## Evaluation Metrics

### Task 1: SQL Benchmark Dataset

**Deliverables**:

- ✅ Benchmark question dataset (`sql_questions.csv`)
- ✅ Ground truth SQL queries
- ✅ Query execution results
- ✅ Evaluation framework

### Task 2: Query Decomposition

**Decomposition Components**:

1. **Intent**: What is being asked (Count, Retrieve, Sum, etc.)
2. **Tables**: Which tables are involved
3. **Columns**: Which columns are needed
4. **Filters**: WHERE conditions
5. **Joins**: JOIN relationships
6. **Aggregations**: COUNT, SUM, AVG, etc.

**Example**:

```json
{
  "question": "How many customers are from USA?",
  "intent": "Count total customers by country",
  "tables": ["customers"],
  "columns": ["customerNumber"],
  "filters": ["country = 'USA'"],
  "joins": [],
  "aggregations": ["COUNT(*)"]
}
```

### Task 3: SQL Pipeline Evaluation

**Metrics**:

- ✅ SQL execution success rate
- ✅ Correct table and column selection
- ✅ Join correctness
- ✅ Retry/self-correction success rate
- ✅ Query generation latency
- ✅ Correct result accuracy

### Task 4: Agent Performance

**Evaluation Criteria**:

- ✅ Query understanding accuracy
- ✅ Correct SQL generation
- ✅ Proper retry mechanism
- ✅ Error handling robustness
- ✅ Natural language summarization quality
- ✅ API response time

## Evaluation Framework

The system includes a comprehensive evaluation framework with the following metrics:

1. **Execution Success Rate**: % of queries executed successfully
2. **First Attempt Success**: % of queries succeeding on first try
3. **Retry Rate**: % of queries requiring retry
4. **Average Execution Time**: Mean time to generate and execute query
5. **Total Failed**: Count of completely failed queries
6. **Self-Correction Rate**: % of queries fixed via retry mechanism

## Example Queries

### Simple Queries

```bash
# List all customers
curl -X POST "http://localhost:8000/agent/sql" \
  -H "Content-Type: application/json" \
  -d '{"question": "Show all customers"}'

# Count customers
curl -X POST "http://localhost:8000/agent/sql" \
  -H "Content-Type: application/json" \
  -d '{"question": "How many customers do we have?"}'
```

### Complex Queries

```bash
# Multi-table join with filtering
curl -X POST "http://localhost:8000/agent/sql" \
  -H "Content-Type: application/json" \
  -d '{"question": "Show all orders from customers in USA with their status"}'

# Aggregation with grouping
curl -X POST "http://localhost:8000/agent/sql" \
  -H "Content-Type: application/json" \
  -d '{"question": "Count orders by country"}'

# Date-based filtering
curl -X POST "http://localhost:8000/agent/sql" \
  -H "Content-Type: application/json" \
  -d '{"question": "Show orders placed in 2003"}'
```

## Troubleshooting

### Database Connection Issues

```python
from app.database import db
from app.schema import get_schema

# Test connection
try:
    schema = get_schema()
    print("✓ Database connected successfully")
except Exception as e:
    print(f"✗ Database connection failed: {e}")
```

### LLM API Issues

```python
from app.llm import llm

# Test LLM connection
try:
    response = llm.invoke("Test message")
    print("✓ LLM API connected")
except Exception as e:
    print(f"✗ LLM API error: {e}")
```

### Query Generation Issues

```python
from app.sql_generator import generate_sql

# Debug SQL generation
question = "Your question"
sql = generate_sql(question)
print(f"Generated SQL:\n{sql}")
```

## Performance Optimization

1. **Schema Caching**: Database schema is cached to avoid repeated queries
2. **Few-Shot Prompting**: LLM uses examples for better accuracy
3. **Error Context**: Retry attempts include error context for better fixes
4. **Query Timeout**: Prevents long-running queries from blocking

## Security Considerations

1. **Query Validation**: Only SELECT queries allowed
2. **Keyword Blocking**: DELETE, DROP, UPDATE, INSERT blocked
3. **SQL Injection Prevention**: Pattern matching for dangerous queries
4. **Error Messages**: Safe error messages (no schema leakage)
5. **Timeout Protection**: Query timeout prevents DOS

## Future Enhancements

- [ ] Multi-turn conversation support
- [ ] Query cost estimation
- [ ] Result caching
- [ ] Custom schema instructions
- [ ] Query performance analysis
- [ ] Batch query processing
- [ ] WebSocket support for streaming results
- [ ] Advanced error recovery strategies
- [ ] Query plan visualization
- [ ] A/B testing framework for LLM improvements

## Contributing

Contributions are welcome! Please ensure:

1. Code follows PEP 8 style guide
2. All functions have docstrings
3. Logging is properly implemented
4. Error handling is comprehensive

## License

This project is provided for educational purposes.

## Support

For issues or questions:

1. Check the logs in `logs/` directory
2. Run the health check endpoint
3. Test database connection
4. Verify environment variables

## Authors

- Text-to-SQL Agent System
- Agentic AI System Implementation
- FastAPI Integration

---

**Version**: 1.0.0
**Last Updated**: 2024
