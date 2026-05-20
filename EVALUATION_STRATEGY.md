# Evaluation Strategy for Text-to-SQL Agents

## Executive Summary

This document outlines a comprehensive evaluation strategy for Text-to-SQL agent systems. It defines metrics, methodologies, and benchmarks to assess system performance and identify areas for improvement.

---

## 1. Evaluation Objectives

### Primary Goals

1. **Assess SQL Correctness**: Evaluate whether generated SQL queries are syntactically and semantically correct
2. **Measure Execution Success**: Track how many queries execute without errors
3. **Evaluate Accuracy**: Determine if results match expected outputs
4. **Evaluate Robustness**: Test system behavior with ambiguous or edge-case questions
5. **Monitor Performance**: Track query generation latency and system responsiveness
6. **Measure Self-Correction**: Evaluate agent's ability to fix errors through retry mechanism

### Secondary Goals

1. **Identify Failure Patterns**: Understand which types of questions cause failures
2. **Optimize Prompting**: Refine LLM prompts based on error analysis
3. **Improve Coverage**: Expand system's ability to handle diverse queries
4. **Track Degradation**: Monitor performance changes over time

---

## 2. Evaluation Dimensions

### 2.1 SQL Correctness

**Definition**: The generated SQL query is syntactically valid and matches the question intent.

**Metrics**:

- **SQL Validity Score**: % of queries with valid syntax (0-100%)
- **Correct Table Selection**: % of queries using correct tables (0-100%)
- **Correct Column Selection**: % of queries selecting correct columns (0-100%)
- **Correct Filter Usage**: % of queries with proper WHERE clauses (0-100%)
- **Join Correctness**: % of multi-table queries with correct JOINs (0-100%)

**Evaluation Method**:

1. Parse generated SQL for syntax errors
2. Compare table names against schema
3. Verify column names exist in selected tables
4. Check filter logic against question intent
5. Validate join conditions

**Example**:

```
Question: "Show customers from USA"
Generated: SELECT * FROM customers WHERE country = 'USA'
Evaluation:
  ✓ Valid syntax
  ✓ Correct table
  ✓ Correct columns
  ✓ Correct filter
  Score: 100%
```

### 2.2 Execution Success

**Definition**: The generated SQL query executes without runtime errors.

**Metrics**:

- **Execution Success Rate**: % of queries that execute (0-100%)
- **Query Timeout Rate**: % of queries exceeding timeout (0-100%)
- **SQL Error Rate**: % of queries with SQL errors (0-100%)
- **Connection Issues**: % of queries failing due to connection (0-100%)

**Evaluation Method**:

1. Execute query against test database
2. Measure execution time
3. Capture any error messages
4. Track timeout occurrences

**Thresholds**:

- ✅ Success: Query executes in < 30 seconds
- ⚠️ Warning: Query executes in 30-60 seconds
- ❌ Failed: Query exceeds 60 seconds or errors

### 2.3 Result Accuracy

**Definition**: The query results match the expected/correct answer.

**Metrics**:

- **Result Accuracy Score**: % of queries with correct results (0-100%)
- **Row Count Match**: % of queries returning correct row count (0-100%)
- **Value Accuracy**: % of rows with correct values (0-100%)
- **Ordering Correctness**: % of queries with correct result ordering (0-100%)

**Evaluation Method**:

1. Execute generated SQL
2. Execute ground-truth SQL
3. Compare results row-by-row
4. Use fuzzy matching for numeric values (± tolerance)
5. Check result ordering

**Scoring**:

- Perfect match: 100%
- Minor differences (ordering, formatting): 80%
- Partial results: 50%
- Wrong results: 0%

### 2.4 Query Type Coverage

**Definition**: System's ability to handle different query patterns.

**Query Categories**:

1. **Simple SELECT**: Basic column selection
2. **With WHERE**: Filtering conditions
3. **With ORDER BY**: Result sorting
4. **With LIMIT**: Result limiting
5. **WITH GROUP BY**: Aggregations with grouping
6. **WITH JOIN**: Multiple table queries
7. **WITH HAVING**: Aggregate filtering
8. **Nested**: Subqueries
9. **WITH Functions**: String/date functions
10. **Complex**: Multi-condition, multi-table queries

**Metrics**:

- **Coverage Score**: # of query types supported / total types
- **Type-Specific Success Rate**: Success rate for each category
- **Difficulty Distribution**: Percentage of easy/medium/hard queries

**Example Coverage Report**:

```
Simple SELECT:     90% ✓
WHERE:            85% ✓
ORDER BY:         80% ✓
LIMIT:            95% ✓
GROUP BY:         75% ✓
JOIN:             70% ⚠️
HAVING:           65% ⚠️
Nested:           50% ✗
Functions:        55% ✗
Complex:          45% ✗

Overall Coverage: 71%
```

### 2.5 Error Handling & Recovery

**Definition**: System's ability to detect and correct errors.

**Metrics**:

- **Error Detection Rate**: % of errors caught (0-100%)
- **Retry Success Rate**: % of failed queries fixed via retry (0-100%)
- **Self-Correction Rate**: % of self-corrected queries (0-100%)
- **Max Retry Efficiency**: Attempts needed for correction (1-3)

**Evaluation Method**:

1. Track first attempt failures
2. Monitor retry success rate
3. Compare retry query with original
4. Measure time cost of retries

**Scoring**:

```
First Attempt Success:      70%
After Retry (max 3):        85%
Self-Correction Gain:       15%
Overall Success:            85%
```

### 2.6 Natural Language Quality

**Definition**: Quality of natural language summaries generated from results.

**Metrics**:

- **Relevance Score**: Is summary relevant to question (0-100%)
- **Completeness**: Does summary answer the question (0-100%)
- **Clarity**: Is summary understandable (0-100%)
- **Conciseness**: Is summary appropriately brief (0-100%)

**Evaluation Method**:

1. Manual review by evaluators
2. Automated checks (grammar, length)
3. Comparison with expected summary
4. User satisfaction surveys

**Example**:

```
Question: "How many customers from USA?"
Result: [{"count": 36}]
Summary: "There are 36 customers from the USA."

Evaluation:
  Relevance: 100% ✓
  Completeness: 100% ✓
  Clarity: 100% ✓
  Conciseness: 95% ✓
  Overall: 98%
```

### 2.7 Performance & Latency

**Definition**: System's speed and efficiency.

**Metrics**:

- **Query Generation Time**: Time to generate SQL (ms)
- **Validation Time**: Time for safety checks (ms)
- **Execution Time**: Time to run query (ms)
- **Summarization Time**: Time to generate summary (ms)
- **Total Latency**: End-to-end response time (ms)
- **P50 Latency**: Median response time (ms)
- **P95 Latency**: 95th percentile response time (ms)
- **P99 Latency**: 99th percentile response time (ms)

**Targets**:

```
Generation:        < 100ms (target: < 50ms)
Validation:        < 10ms  (target: < 5ms)
Execution:         < 500ms (target: < 200ms)
Summarization:     < 100ms (target: < 50ms)
Total:             < 1000ms (target: < 500ms)
```

**Optimization Tips**:

- Use schema caching (already implemented)
- Batch requests when possible
- Optimize LLM prompts for clarity
- Use query result limits for large tables

---

## 3. Evaluation Framework

### 3.1 Test Dataset Structure

```csv
question,expected_sql,difficulty,category
"List all customers","SELECT * FROM customers;",easy,simple
"Count customers from USA","SELECT COUNT(*) FROM customers WHERE country = 'USA';",easy,filter
"Show orders with customer names","SELECT o.*, c.customerName FROM orders o JOIN customers c ON o.customerNumber = c.customerNumber;",medium,join
```

### 3.2 Evaluation Pipeline

```
Load Test Cases
    ↓
For Each Question:
    1. Generate SQL using agent
    2. Validate SQL syntax
    3. Execute query
    4. Compare results with expected
    5. Measure latency
    6. Record metrics
    ↓
Aggregate Results
    ↓
Generate Report
    ↓
Export Metrics (JSON/CSV)
```

### 3.3 Scoring System

**Overall Score** (0-100%):

```
Overall Score = (
    SQL_Correctness_Score * 0.25 +
    Execution_Success_Rate * 0.25 +
    Result_Accuracy_Score * 0.30 +
    Error_Recovery_Rate * 0.15 +
    Performance_Score * 0.05
) * 100
```

**Grade Mapping**:

```
90-100%: A (Excellent)
80-89%:  B (Good)
70-79%:  C (Acceptable)
60-69%:  D (Needs Improvement)
< 60%:   F (Poor)
```

---

## 4. Benchmark Dataset

### 4.1 Dataset Composition

**Recommended Distribution**:

- **Simple Queries**: 30% (basic SELECT, WHERE, LIMIT)
- **Moderate Queries**: 40% (JOIN, GROUP BY, ORDER BY)
- **Complex Queries**: 20% (nested, multiple JOINs, aggregations)
- **Edge Cases**: 10% (ambiguous, unusual patterns)

**Recommended Size**:

- Minimum: 50 questions
- Good: 100-200 questions
- Comprehensive: 500+ questions

### 4.2 Query Categories in Benchmark

Based on typical Text-to-SQL systems, include:

1. **Table Discovery**: "Show all [tables]"
2. **Column Selection**: "Get [columns] from [table]"
3. **Filtering**: "Get [columns] where [condition]"
4. **Aggregation**: "Count/Sum/Average [column]"
5. **Grouping**: "Group by [column]"
6. **Joining**: "Show [data] with [related data]"
7. **Sorting**: "Order by [column]"
8. **Combination**: Multiple of above
9. **Subqueries**: Nested queries
10. **Date Handling**: Temporal queries

---

## 5. Evaluation Reports

### 5.1 Report Structure

```json
{
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "total_questions": 100,
    "evaluator": "Text-to-SQL Agent v1.0",
    "database": "production_schema"
  },
  "summary": {
    "overall_score": 82.5,
    "grade": "B",
    "passed": 85,
    "failed": 15
  },
  "metrics": {
    "execution_success_rate": 85.0,
    "sql_correctness": 88.0,
    "result_accuracy": 82.0,
    "error_recovery_rate": 75.0,
    "avg_latency_ms": 450,
    "p95_latency_ms": 890
  },
  "by_category": {
    "simple": { "success_rate": 95, "avg_latency": 200 },
    "moderate": { "success_rate": 85, "avg_latency": 500 },
    "complex": { "success_rate": 65, "avg_latency": 800 }
  },
  "failures": [
    {
      "question": "...",
      "reason": "Incorrect JOIN",
      "error": "..."
    }
  ]
}
```

### 5.2 Report Visualization

**Sample Dashboard Metrics**:

```
╔════════════════════════════════════════════╗
║     TEXT-TO-SQL AGENT EVALUATION           ║
╠════════════════════════════════════════════╣
║ Overall Score:           82.5% (Grade: B)  ║
║ Execution Success:       85.0%             ║
║ SQL Correctness:         88.0%             ║
║ Result Accuracy:         82.0%             ║
║ Error Recovery:          75.0%             ║
║ Avg Latency:             450ms             ║
║ P95 Latency:             890ms             ║
╚════════════════════════════════════════════╝
```

---

## 6. Continuous Evaluation

### 6.1 Regression Testing

**Purpose**: Detect performance degradation

**Frequency**: After each update

**Process**:

1. Run full benchmark suite
2. Compare against baseline
3. Alert if score drops > 5%
4. Investigate regressions

### 6.2 A/B Testing

**Purpose**: Compare prompt versions or LLM models

**Methodology**:

```
Split dataset 50/50:
  Group A: Original system
  Group B: New system

Compare metrics:
  - Success rate
  - Latency
  - Accuracy
  - User satisfaction

Threshold: New system must improve metrics
or at least maintain performance
```

### 6.3 Metric Tracking Over Time

**Track**:

- Weekly success rate trend
- Monthly accuracy improvements
- Quarterly coverage expansion
- Yearly overall score progression

**Visualization**:

```
Success Rate Over Time:
  100% ████████████ (Week 1)
   95% ████████░░░ (Week 2)
   92% ███████░░░░ (Week 3)
   97% ████████░░░ (Week 4)

Trend: ↗ Improving
```

---

## 7. Failure Analysis

### 7.1 Common Failure Patterns

| Pattern              | Frequency | Root Cause              | Fix                      |
| -------------------- | --------- | ----------------------- | ------------------------ |
| Column name mismatch | 15%       | Schema understanding    | Improve schema prompting |
| Missing JOINs        | 12%       | Relationship detection  | Add join examples        |
| Wrong aggregation    | 10%       | Intent misunderstanding | Refine decomposition     |
| Syntax errors        | 8%        | LLM generation          | Better output cleaning   |
| Type mismatches      | 5%        | Type inference          | Add type hints in schema |

### 7.2 Error Investigation Process

```
For each failure:
1. Categorize error type
2. Identify root cause
3. Propose fix
4. Test fix on similar cases
5. Update prompts/examples if needed
6. Retrain if needed
```

---

## 8. Success Criteria

### 8.1 Minimum Acceptance Criteria

✅ **Must Have**:

- [ ] Execution Success Rate ≥ 80%
- [ ] SQL Correctness ≥ 85%
- [ ] Result Accuracy ≥ 80%
- [ ] Avg Latency ≤ 1000ms
- [ ] Error Recovery Rate ≥ 70%

✅ **Should Have**:

- [ ] Coverage of query types ≥ 80%
- [ ] Natural language quality ≥ 85%
- [ ] P95 Latency ≤ 2000ms

✅ **Nice to Have**:

- [ ] P99 Latency ≤ 3000ms
- [ ] Coverage of edge cases ≥ 90%
- [ ] User satisfaction ≥ 90%

### 8.2 Production Readiness

System is production-ready when:

1. ✅ All minimum criteria met
2. ✅ Error handling robust
3. ✅ Logging comprehensive
4. ✅ Security validated
5. ✅ Performance acceptable
6. ✅ Documentation complete

---

## 9. Improvement Roadmap

### Phase 1: Foundation (Weeks 1-2)

- [x] Implement basic evaluation framework
- [x] Create benchmark dataset (50 questions)
- [x] Establish baseline metrics

### Phase 2: Optimization (Weeks 3-4)

- [ ] Improve prompt templates
- [ ] Expand to 200 questions
- [ ] Target 85% success rate

### Phase 3: Expansion (Weeks 5-6)

- [ ] Add complex query support
- [ ] Expand to 500 questions
- [ ] Add edge case handling

### Phase 4: Polish (Weeks 7-8)

- [ ] Fine-tune LLM prompts
- [ ] Optimize performance
- [ ] Document best practices

---

## 10. Conclusion

This evaluation framework provides a comprehensive approach to assessing Text-to-SQL agent systems. By tracking multiple dimensions and continuously improving based on evaluation results, we can build increasingly capable systems that serve users effectively.

**Key Takeaways**:

1. Multi-dimensional evaluation is essential
2. Continuous monitoring prevents degradation
3. Diverse datasets expose system limitations
4. Root cause analysis enables targeted improvements
5. Clear success criteria guide development

---

## Appendix: Evaluation Tools

### Available Scripts

```bash
# Run full evaluation
python evaluate.py sql_questions.csv logs

# Evaluate specific question
python -c "from app.agent import run_agent; print(run_agent('Your question'))"

# Run evaluation programmatically
python -c "
from app.evaluation import EvaluationFramework
evaluator = EvaluationFramework()
evaluator.evaluate_batch(['q1', 'q2'])
evaluator.print_report()
"
```

### Output Files

- `evaluation_report.json`: Complete report with metrics
- `evaluation_results.csv`: Detailed results for each question
- `logs/agent_*.log`: System logs with execution details

---

**Document Version**: 1.0
**Last Updated**: 2024
**Status**: Active
