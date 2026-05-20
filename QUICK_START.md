# Quick Start Guide - Text-to-SQL Agent

## 🚀 5-Minute Setup

### Step 1: Clone and Navigate

```bash
cd Text_To_SQL
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
# - DATABASE_URL: Your PostgreSQL connection
# - GROQ_API_KEY: Your Groq API key from https://console.groq.com
```

### Step 5: Start the Server

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 6: Test the API

Open your browser and go to:

```
http://localhost:8000/docs
```

---

## 📊 Using the API

### Example 1: Simple Query

```bash
curl -X POST "http://localhost:8000/agent/sql" \
  -H "Content-Type: application/json" \
  -d '{"question": "How many customers do we have?"}'
```

### Example 2: Complex Query with Join

```bash
curl -X POST "http://localhost:8000/agent/sql" \
  -H "Content-Type: application/json" \
  -d '{"question": "Show all orders from customers in Germany"}'
```

### Example 3: Aggregation

```bash
curl -X POST "http://localhost:8000/agent/sql" \
  -H "Content-Type: application/json" \
  -d '{"question": "Count customers by country"}'
```

---

## 🧪 Running Evaluation

```bash
# Evaluate all questions from csv
python evaluate.py sql_questions.csv logs

# Check results
# - logs/evaluation_report.json (detailed report)
# - logs/evaluation_results.csv (raw results)
```

---

## 📋 System Components

| Component               | File                   | Purpose                     |
| ----------------------- | ---------------------- | --------------------------- |
| **Agent Orchestrator**  | `app/agent.py`         | Main agentic system         |
| **Query Decomposition** | `app/decompose.py`     | Break down natural language |
| **SQL Generation**      | `app/sql_generator.py` | Generate SQL using LLM      |
| **Validation**          | `app/validator.py`     | Safety checks               |
| **Execution**           | `app/executer.py`      | Run SQL queries             |
| **Summarization**       | `app/summarize.py`     | Convert to natural language |
| **FastAPI App**         | `app/main.py`          | REST API endpoints          |
| **Evaluation**          | `app/evaluation.py`    | Evaluation framework        |

---

## 🔍 Monitoring & Debugging

### Check Logs

```bash
# View today's log
cat logs/agent_YYYYMMDD.log

# Follow logs in real-time
tail -f logs/agent_YYYYMMDD.log
```

### Test Database Connection

```bash
python -c "from app.database import db; print('✓ Connected')"
```

### Test LLM Connection

```bash
python -c "from app.llm import llm; print(llm.invoke('test'))"
```

### Manual Query Test

```python
from app.agent import run_agent

result = run_agent("How many customers from USA?")
print(result)
```

---

## 📈 Understanding Response

```json
{
  "question": "How many customers from USA?",
  "sql": "SELECT COUNT(*) FROM customers WHERE country = 'USA'",
  "result": [{ "COUNT": 36 }],
  "summary": "There are 36 customers from the USA.",
  "status": "success", // success, failed, blocked
  "attempts": 1, // 1-3 attempts
  "execution_time_ms": 245.67, // Total time
  "error": null // Error message if any
}
```

**Status Values**:

- `success`: Query succeeded on first attempt
- `success_after_retry`: Query succeeded after retry
- `failed`: Query failed after all retry attempts
- `blocked`: Query blocked by safety validation

---

## ⚙️ Configuration

### Environment Variables (in .env)

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/db
GROQ_API_KEY=your_api_key
GROQ_MODEL_NAME=mixtral-8x7b-32768  # or gemma-7b-it, llama2-70b-4096
MAX_RETRIES=3                        # Max retry attempts
QUERY_TIMEOUT=30                     # Timeout in seconds
LOG_LEVEL=INFO                       # DEBUG, INFO, WARNING, ERROR
```

---

## 🛡️ Safety Features

The system includes multiple safety layers:

1. **Keyword Blocking**: Blocks DELETE, DROP, UPDATE, INSERT
2. **Syntax Validation**: Ensures valid SQL
3. **SQL Injection Prevention**: Pattern matching for dangerous queries
4. **Query Timeout**: Prevents long-running queries
5. **Error Handling**: Graceful error recovery

❌ **Cannot Execute**:

- DELETE queries
- DROP operations
- UPDATE statements
- INSERT operations
- Database modifications

✅ **Only Allows**:

- SELECT queries (read-only)
- Safely validated operations

---

## 🚨 Common Issues & Solutions

### Issue: "DATABASE_URL not set"

**Solution**: Create .env file with valid DATABASE_URL

### Issue: "GROQ_API_KEY not set"

**Solution**: Get API key from https://console.groq.com

### Issue: "Connection refused"

**Solution**: Ensure PostgreSQL is running and DATABASE_URL is correct

### Issue: "Query timeout"

**Solution**: Increase QUERY_TIMEOUT in .env (default 30s)

### Issue: "Failed queries in evaluation"

**Solution**: Check logs/, verify questions match schema

---

## 📚 Documentation Files

- **SYSTEM_DOCUMENTATION.md**: Complete system documentation
- **EVALUATION_STRATEGY.md**: Evaluation framework and metrics
- **.env.example**: Configuration template
- **sql_questions.csv**: Benchmark questions
- **database_schema.txt**: Database schema

---

## 🎯 Next Steps

1. ✅ Start the server
2. ✅ Test with sample queries
3. ✅ Run evaluation suite
4. ✅ Check evaluation reports
5. ✅ Review logs for insights
6. ✅ Adjust as needed

---

## 💡 Tips for Best Results

1. **Be Specific**: Ask clear, unambiguous questions
2. **Use Table Names**: Mention table names when possible
3. **Simple is Better**: Break complex questions into steps
4. **Check Results**: Verify results make sense
5. **Monitor Performance**: Watch execution times

---

## 📞 Support

For help:

1. Check **SYSTEM_DOCUMENTATION.md**
2. Review **EVALUATION_STRATEGY.md**
3. Check logs in `logs/` directory
4. Test endpoints individually

---

**Ready to go!** 🎉

Run: `python -m uvicorn app.main:app --reload`

Then visit: `http://localhost:8000/docs`
