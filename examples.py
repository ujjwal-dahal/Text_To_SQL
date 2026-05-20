"""
Examples and Test Cases for Text-to-SQL Agent

Demonstrates how to use the Text-to-SQL agent system
with various query types and use cases.
"""

from app.agent import run_agent
from app.decompose import decompose_query
from app.evaluation import EvaluationFramework
from app.logger import setup_logger

logger = setup_logger(__name__)


def example_simple_query():
    """Example 1: Simple SELECT query"""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Simple SELECT Query")
    print("=" * 80)

    question = "Show all customers"
    print(f"Question: {question}\n")

    result = run_agent(question)

    print(f"SQL Query: {result['sql']}")
    print(f"Status: {result['status']}")
    print(f"Attempts: {result['attempts']}")
    print(f"Results: {result['result'][:2] if result['result'] else 'No results'}")
    print(f"Summary: {result['summary']}")


def example_filter_query():
    """Example 2: Query with WHERE clause"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Query with Filtering")
    print("=" * 80)

    question = "How many customers are from USA?"
    print(f"Question: {question}\n")

    result = run_agent(question)

    print(f"SQL Query: {result['sql']}")
    print(f"Status: {result['status']}")
    print(f"Results: {result['result']}")
    print(f"Summary: {result['summary']}")


def example_join_query():
    """Example 3: Query with JOIN"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Query with JOIN")
    print("=" * 80)

    question = "Show all orders from customers in Germany"
    print(f"Question: {question}\n")

    result = run_agent(question)

    print(f"SQL Query: {result['sql']}")
    print(f"Status: {result['status']}")
    print(f"Attempts: {result['attempts']}")
    print(f"Summary: {result['summary']}")


def example_aggregation_query():
    """Example 4: Query with aggregation"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Query with Aggregation")
    print("=" * 80)

    question = "Count customers by country"
    print(f"Question: {question}\n")

    result = run_agent(question)

    print(f"SQL Query: {result['sql']}")
    print(f"Status: {result['status']}")
    print(f"Results (top 5):")
    if result["result"]:
        for row in result["result"][:5]:
            print(f"  {row}")


def example_decomposition():
    """Example 5: Query decomposition"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Query Decomposition")
    print("=" * 80)

    question = "Show all customers from USA with their sales representatives"
    print(f"Question: {question}\n")

    decomposition = decompose_query(question)
    print(decomposition)


def example_evaluation():
    """Example 6: Evaluation framework"""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Evaluation Framework")
    print("=" * 80)

    # Create evaluator
    evaluator = EvaluationFramework()

    # Define test questions
    test_questions = [
        "Show all customers",
        "How many customers from USA?",
        "List all products",
        "Get all employees",
        "Show all orders",
    ]

    print(f"Evaluating {len(test_questions)} questions...\n")

    # Evaluate
    results = evaluator.evaluate_batch(test_questions)

    # Calculate metrics
    metrics = evaluator.calculate_metrics()

    print(f"Evaluation Results:")
    print(f"  Total Questions: {int(metrics['total_questions'])}")
    print(f"  Success Rate: {metrics['execution_success_rate']:.1f}%")
    print(f"  First Attempt Success: {metrics['first_attempt_success_rate']:.1f}%")
    print(f"  Avg Execution Time: {metrics['average_execution_time_ms']:.2f}ms")
    print(f"  Failed: {int(metrics['total_failed'])}")


def example_batch_evaluation():
    """Example 7: Batch evaluation from CSV"""
    print("\n" + "=" * 80)
    print("EXAMPLE 7: Batch Evaluation from CSV")
    print("=" * 80)

    import csv

    # Load questions from CSV
    questions = []
    try:
        with open("sql_questions.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "question" in row:
                    questions.append(row["question"].strip())
    except FileNotFoundError:
        print("sql_questions.csv not found. Using sample questions.")
        questions = ["Show all customers", "Count customers from USA"]

    print(f"Loaded {len(questions)} questions from CSV\n")

    # Evaluate
    evaluator = EvaluationFramework()
    evaluator.evaluate_batch(questions[:10])  # Evaluate first 10

    # Print report
    evaluator.print_report()


def example_error_handling():
    """Example 8: Error handling and recovery"""
    print("\n" + "=" * 80)
    print("EXAMPLE 8: Error Handling and Recovery")
    print("=" * 80)

    # A question that might require retry
    question = "What are the names of employees and their office locations?"
    print(f"Question: {question}\n")

    result = run_agent(question)

    print(f"SQL Query: {result['sql']}")
    print(f"Status: {result['status']}")
    print(f"Attempts: {result['attempts']}")

    if result["attempts"] > 1:
        print(f"✓ Query required retry but succeeded!")
    else:
        print(f"✓ Query succeeded on first attempt")

    if result["error"]:
        print(f"Final error (if any): {result['error']}")


def example_performance_analysis():
    """Example 9: Performance analysis"""
    print("\n" + "=" * 80)
    print("EXAMPLE 9: Performance Analysis")
    print("=" * 80)

    import time

    questions = [
        "Show all customers",
        "Count customers from USA",
        "List employees from Boston office",
        "Show orders from 2023",
        "Get product information",
    ]

    times = []

    print("Measuring performance...\n")

    for question in questions:
        start = time.time()
        result = run_agent(question)
        elapsed = (time.time() - start) * 1000
        times.append(elapsed)

        status_symbol = (
            "✓" if result["status"] in ["success", "success_after_retry"] else "✗"
        )
        print(f"{status_symbol} {question[:40]:<40} {elapsed:>8.2f}ms")

    print(f"\nPerformance Summary:")
    print(f"  Avg Time: {sum(times)/len(times):.2f}ms")
    print(f"  Min Time: {min(times):.2f}ms")
    print(f"  Max Time: {max(times):.2f}ms")


def run_all_examples():
    """Run all examples"""
    examples = [
        ("Simple Query", example_simple_query),
        ("Filter Query", example_filter_query),
        ("Join Query", example_join_query),
        ("Aggregation Query", example_aggregation_query),
        ("Query Decomposition", example_decomposition),
        ("Error Handling", example_error_handling),
        ("Performance Analysis", example_performance_analysis),
    ]

    print("\n" + "=" * 80)
    print("TEXT-TO-SQL AGENT - EXAMPLES AND TEST CASES")
    print("=" * 80)

    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n✗ Example failed: {str(e)}")
            logger.error(f"Example '{name}' failed: {str(e)}", exc_info=True)


if __name__ == "__main__":
    # Uncomment to run specific examples

    # Run all examples
    run_all_examples()

    # Or run individual examples:
    # example_simple_query()
    # example_filter_query()
    # example_join_query()
    # example_aggregation_query()
    # example_decomposition()
    # example_batch_evaluation()
    # example_error_handling()
    # example_performance_analysis()

    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)
