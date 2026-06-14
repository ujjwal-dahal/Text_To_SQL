# Text-to-SQL Agent

An AI-powered Text-to-SQL Agent that converts natural language questions into executable SQL queries.  
It understands user questions, generates SQL, executes it on a database, and returns meaningful results.

The project also includes evaluation datasets, benchmarking tools, schema-aware query generation, and performance measurement utilities.

---

## Features

- Natural Language to SQL conversion
- Schema-aware query generation
- Automatic SQL execution on databases
- Evaluation and benchmarking system
- Modular and scalable architecture
- Dataset-driven testing support
- Easy local setup
- Modern Python dependency management

---

## Project Structure

```
.
├── app/
│   ├── agents/
│   ├── prompts/
│   ├── database/
│   ├── tools/
│   └── services/
│
├── evaluate.py
├── examples.py
├── test_query.py
│
├── database_schema.txt
├── seed.sql
├── sql_questions.csv
│
├── EVALUATION_STRATEGY.md
├── IMPLEMENTATION_SUMMARY.md
├── SYSTEM_DOCUMENTATION.md
│
├── pyproject.toml
├── uv.lock
├── requirements.txt
├── .python-version
└── README.md
```

---

## System Workflow

```
User Question
   ↓
Text-to-SQL Agent
   ↓
Schema Understanding
   ↓
SQL Generation
   ↓
Database Execution
   ↓
Result Processing
   ↓
Final Answer
```

---

## Technology Stack

### Programming Language
- Python 3.10+

### AI / LLM Models
- OpenAI GPT models
- Anthropic Claude models
- Other compatible LLM APIs

### Databases
- SQLite
- PostgreSQL
- MySQL

### Core Libraries
- SQLAlchemy
- Pandas
- python-dotenv

### Package Management
- UV (recommended)
- pip

---

## Prerequisites

Ensure the following are installed:

- Python 3.10+
- Git
- UV (optional but recommended)
- SQLite / PostgreSQL / MySQL

Check versions:

```bash
python --version
git --version
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/text-to-sql-agent.git
cd text-to-sql-agent
```

---

### 2. Create Virtual Environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS
```bash
python -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

#### Option A: UV (Recommended)
```bash
uv sync
```

or

```bash
uv pip install -r requirements.txt
```

#### Option B: Pip
```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_api_key
DATABASE_URL=your_database_connection_string
MODEL_NAME=gpt-4
```

---

## Database Setup

### SQLite
```bash
sqlite3 database.db < seed.sql
```

### PostgreSQL
```bash
psql -U username -d database_name -f seed.sql
```

### MySQL
```bash
mysql -u username -p database_name < seed.sql
```

---

## Usage

### Run a Single Query Test

```bash
python test_query.py
```

Example:

Input:
```
Show all employees with salary greater than 50000
```

Generated SQL:
```sql
SELECT * FROM employees WHERE salary > 50000;
```

---

### Run Example Queries

```bash
python examples.py
```

Includes:
- Simple queries
- Filtering
- Aggregations
- Joins
- Complex analytical queries

---

### Run Evaluation Benchmark

```bash
python evaluate.py
```

Evaluation metrics:
- SQL Accuracy
- Execution Accuracy
- Semantic Similarity
- Result Matching
- Overall Performance Score

Dataset used:
```
sql_questions.csv
```

---

## Documentation

- `SYSTEM_DOCUMENTATION.md` → Architecture & system design
- `IMPLEMENTATION_SUMMARY.md` → Development decisions
- `EVALUATION_STRATEGY.md` → Benchmarking and metrics

---

## Example

### Input
```
What are the top 5 highest-paid employees?
```

### Output SQL
```sql
SELECT *
FROM employees
ORDER BY salary DESC
LIMIT 5;
```

### Result
```
Employee A
Employee B
Employee C
Employee D
Employee E
```

---

## Development Workflow

```bash
git checkout -b feature/new-feature
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

---

## Future Improvements

- Multi-turn conversation support
- Query correction system
- Memory-enabled agent
- Query optimization layer
- Multi-database routing
- RAG-based schema retrieval
- Fine-tuned Text-to-SQL models

---

## Goals

- High SQL generation accuracy
- Reliable execution results
- Low hallucination rate
- Strong generalization across schemas

---

## License

For educational and research purposes only.

---

## Author

**Ujjwal Dahal**  
FuseMachine AI Fellowship Assignment  

GitHub: https://github.com/ujjwal-dahal
