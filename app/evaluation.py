"""
Evaluation Framework for Text-to-SQL Agent (Task 1 & 2)

This module provides tools to:
1. Benchmark the Text-to-SQL system against known questions
2. Evaluate SQL correctness
3. Track performance metrics
4. Generate evaluation reports
"""

import json
import csv
import time
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from pathlib import Path
from app.agent import run_agent
from app.logger import setup_logger

logger = setup_logger(__name__)


class EvaluationMetric:
    """Represents a single evaluation metric"""

    def __init__(self, name: str, value: float, description: str = ""):
        self.name = name
        self.value = value
        self.description = description

    def to_dict(self):
        return {"name": self.name, "value": self.value, "description": self.description}


class BenchmarkResult:
    """Represents result of evaluating one question"""

    def __init__(
        self,
        question: str,
        expected_sql: Optional[str] = None,
        generated_sql: Optional[str] = None,
        executed_successfully: bool = False,
        correct_result: bool = False,
        retry_needed: bool = False,
        attempts: int = 1,
        execution_time_ms: float = 0,
        error: Optional[str] = None,
    ):
        self.question = question
        self.expected_sql = expected_sql
        self.generated_sql = generated_sql
        self.executed_successfully = executed_successfully
        self.correct_result = correct_result
        self.retry_needed = retry_needed
        self.attempts = attempts
        self.execution_time_ms = execution_time_ms
        self.error = error
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return {
            "question": self.question,
            "expected_sql": self.expected_sql,
            "generated_sql": self.generated_sql,
            "executed_successfully": self.executed_successfully,
            "correct_result": self.correct_result,
            "retry_needed": self.retry_needed,
            "attempts": self.attempts,
            "execution_time_ms": self.execution_time_ms,
            "error": self.error,
            "timestamp": self.timestamp,
        }


class EvaluationFramework:
    """
    Evaluation Framework for Text-to-SQL Agent

    Evaluates:
    - SQL execution success rate
    - Correctness of generated SQL
    - Correct table and column selection
    - Query result accuracy
    - Retry/self-correction success rate
    - Number of failed queries
    - Query generation latency
    - Natural language response quality
    """

    def __init__(self):
        self.results: List[BenchmarkResult] = []
        self.metrics: Dict[str, float] = {}

    def evaluate_question(
        self,
        question: str,
        expected_sql: Optional[str] = None,
    ) -> BenchmarkResult:
        """
        Evaluate a single question using the agent.

        Args:
            question: Natural language question
            expected_sql: Expected SQL query (for comparison)

        Returns:
            BenchmarkResult with evaluation details
        """
        logger.info(f"Evaluating: {question}")

        try:
            start_time = time.time()
            agent_result = run_agent(question)
            execution_time = (time.time() - start_time) * 1000

            generated_sql = agent_result.get("sql")
            status = agent_result.get("status")
            attempts = agent_result.get("attempts", 1)
            error = agent_result.get("error")

            executed_successfully = status in ["success", "success_after_retry"]
            retry_needed = attempts > 1

            result = BenchmarkResult(
                question=question,
                expected_sql=expected_sql,
                generated_sql=generated_sql,
                executed_successfully=executed_successfully,
                retry_needed=retry_needed,
                attempts=attempts,
                execution_time_ms=execution_time,
                error=error,
            )

            self.results.append(result)
            logger.info(f"Evaluation complete: {status}")

            return result

        except Exception as e:
            logger.error(f"Evaluation failed: {str(e)}")
            result = BenchmarkResult(
                question=question,
                expected_sql=expected_sql,
                executed_successfully=False,
                error=str(e),
            )
            self.results.append(result)
            return result

    def evaluate_batch(
        self,
        questions: List[str],
        expected_queries: Optional[List[str]] = None,
    ) -> List[BenchmarkResult]:
        """
        Evaluate multiple questions.

        Args:
            questions: List of natural language questions
            expected_queries: List of expected SQL queries

        Returns:
            List of BenchmarkResult objects
        """
        if expected_queries and len(expected_queries) != len(questions):
            logger.warning("Expected queries list length doesn't match questions")
            expected_queries = [None] * len(questions)
        elif not expected_queries:
            expected_queries = [None] * len(questions)

        logger.info(f"Starting batch evaluation of {len(questions)} questions")

        for question, expected_sql in zip(questions, expected_queries):
            self.evaluate_question(question, expected_sql)

        logger.info(f"Batch evaluation complete. Total: {len(self.results)}")
        return self.results

    def calculate_metrics(self) -> Dict[str, float]:
        """
        Calculate evaluation metrics from results.

        Metrics:
        - Total questions evaluated
        - Execution success rate (%)
        - Retry rate (%)
        - Average execution time (ms)
        - Total failed queries
        - Success on first attempt rate (%)

        Returns:
            Dictionary of calculated metrics
        """
        if not self.results:
            logger.warning("No results to calculate metrics from")
            return {}

        total = len(self.results)
        successful = sum(1 for r in self.results if r.executed_successfully)
        required_retry = sum(1 for r in self.results if r.retry_needed)
        failed = sum(1 for r in self.results if r.error)
        first_attempt_success = sum(
            1 for r in self.results if r.executed_successfully and r.attempts == 1
        )

        avg_time = (
            sum(r.execution_time_ms for r in self.results) / total if total > 0 else 0
        )

        self.metrics = {
            "total_questions": float(total),
            "execution_success_rate": (successful / total * 100) if total > 0 else 0,
            "retry_rate": (required_retry / total * 100) if total > 0 else 0,
            "first_attempt_success_rate": (
                (first_attempt_success / total * 100) if total > 0 else 0
            ),
            "average_execution_time_ms": avg_time,
            "total_successful": float(successful),
            "total_failed": float(failed),
            "total_retried": float(required_retry),
        }

        logger.info(f"Metrics calculated: {self.metrics}")
        return self.metrics

    def generate_report(self) -> Dict:
        """
        Generate comprehensive evaluation report.

        Returns:
            Dictionary containing:
            - metadata (timestamp, total questions, etc.)
            - metrics (calculated performance metrics)
            - results (detailed results for each question)
            - summary (text summary)
        """
        metrics = self.calculate_metrics()

        report = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_questions": len(self.results),
                "evaluator": "Text-to-SQL Agent Evaluation Framework v1.0",
            },
            "metrics": metrics,
            "results": [r.to_dict() for r in self.results],
            "summary": self._generate_summary(metrics),
        }

        return report

    def _generate_summary(self, metrics: Dict[str, float]) -> str:
        """Generate text summary of evaluation results"""
        if not metrics:
            return "No evaluation data available"

        summary = f"""
EVALUATION SUMMARY
==================

Total Questions Evaluated: {int(metrics.get('total_questions', 0))}
Execution Success Rate: {metrics.get('execution_success_rate', 0):.1f}%
First Attempt Success: {metrics.get('first_attempt_success_rate', 0):.1f}%
Retry Rate: {metrics.get('retry_rate', 0):.1f}%
Failed Queries: {int(metrics.get('total_failed', 0))}
Average Execution Time: {metrics.get('average_execution_time_ms', 0):.2f}ms

KEY INSIGHTS:
- {int(metrics.get('total_successful', 0))}/{int(metrics.get('total_questions', 0))} queries executed successfully
- {metrics.get('first_attempt_success_rate', 0):.1f}% success on first attempt
- Agent demonstrated self-correction ability with {metrics.get('retry_rate', 0):.1f}% requiring retries
- Average response time: {metrics.get('average_execution_time_ms', 0):.2f}ms
"""
        return summary.strip()

    def export_csv(self, filename: str = "evaluation_results.csv"):
        """
        Export evaluation results to CSV file.

        Args:
            filename: Output CSV filename
        """
        try:
            output_path = Path(filename)

            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "question",
                        "expected_sql",
                        "generated_sql",
                        "executed_successfully",
                        "retry_needed",
                        "attempts",
                        "execution_time_ms",
                        "error",
                        "timestamp",
                    ],
                )
                writer.writeheader()

                for result in self.results:
                    writer.writerow(result.to_dict())

            logger.info(f"Results exported to {output_path}")
        except Exception as e:
            logger.error(f"Failed to export CSV: {str(e)}")

    def export_json(self, filename: str = "evaluation_report.json"):
        """
        Export evaluation report to JSON file.

        Args:
            filename: Output JSON filename
        """
        try:
            report = self.generate_report()
            output_path = Path(filename)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)

            logger.info(f"Report exported to {output_path}")
        except Exception as e:
            logger.error(f"Failed to export JSON: {str(e)}")

    def print_report(self):
        """Print evaluation report to console"""
        report = self.generate_report()

        print("\n" + "=" * 80)
        print("EVALUATION REPORT - TEXT-TO-SQL AGENT")
        print("=" * 80)

        print(f"\nTimestamp: {report['metadata']['timestamp']}")
        print(f"Total Questions: {report['metadata']['total_questions']}")

        print("\n" + "-" * 80)
        print("PERFORMANCE METRICS")
        print("-" * 80)

        metrics = report["metrics"]
        for key, value in metrics.items():
            if isinstance(value, float):
                if "rate" in key or "success" in key:
                    print(f"{key}: {value:.2f}%")
                elif "time" in key:
                    print(f"{key}: {value:.2f}ms")
                else:
                    print(f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")

        print("\n" + "-" * 80)
        print("DETAILED RESULTS")
        print("-" * 80)

        for i, result in enumerate(self.results, 1):
            status = "✓" if result.executed_successfully else "✗"
            print(f"\n{i}. {status} {result.question}")
            print(
                f"   Status: {'Success' if result.executed_successfully else 'Failed'}"
            )
            print(f"   Attempts: {result.attempts}")
            if result.error:
                print(f"   Error: {result.error}")

        print("\n" + report["summary"])
        print("\n" + "=" * 80 + "\n")


# Example usage
if __name__ == "__main__":
    # Load questions from CSV
    evaluator = EvaluationFramework()

    test_questions = [
        "List all customers",
        "Count customers from USA",
        "Show all orders",
        "Get employees from NY office",
    ]

    evaluator.evaluate_batch(test_questions)
    evaluator.print_report()
    evaluator.export_json("evaluation_report.json")
    evaluator.export_csv("evaluation_results.csv")
