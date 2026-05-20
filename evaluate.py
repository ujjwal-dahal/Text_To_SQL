"""
Evaluation Script for Text-to-SQL Agent System

This script demonstrates how to:
1. Load benchmark questions from CSV
2. Evaluate the agent against these questions
3. Generate comprehensive evaluation reports
4. Export results for analysis
"""

import csv
import sys
from pathlib import Path
from app.evaluation import EvaluationFramework
from app.logger import setup_logger

logger = setup_logger(__name__)


def load_questions_from_csv(csv_file: str) -> list:
    """Load questions from SQL benchmark CSV file"""
    try:
        questions = []
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "question" in row:
                    questions.append(row["question"].strip())

        logger.info(f"Loaded {len(questions)} questions from {csv_file}")
        return questions
    except Exception as e:
        logger.error(f"Failed to load CSV: {str(e)}")
        return []


def run_evaluation(csv_file: str = "sql_questions.csv", output_dir: str = "logs"):
    """
    Run complete evaluation of the Text-to-SQL agent.

    Args:
        csv_file: Path to CSV file with benchmark questions
        output_dir: Directory to save evaluation reports
    """

    logger.info("=" * 80)
    logger.info("STARTING TEXT-TO-SQL AGENT EVALUATION")
    logger.info("=" * 80)

    # Load questions
    questions = load_questions_from_csv(csv_file)

    if not questions:
        logger.error("No questions loaded. Exiting.")
        return

    # Create evaluator
    evaluator = EvaluationFramework()

    # Evaluate batch
    logger.info(f"\nEvaluating {len(questions)} questions...")
    evaluator.evaluate_batch(questions)

    # Generate and print report
    logger.info("\n\nGenerating evaluation report...")
    evaluator.print_report()

    # Export results
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    evaluator.export_json(str(output_path / "evaluation_report.json"))
    evaluator.export_csv(str(output_path / "evaluation_results.csv"))

    logger.info("\n✓ Evaluation complete!")
    logger.info(f"Reports saved to {output_dir}/")


if __name__ == "__main__":
    # Run evaluation
    csv_file = "sql_questions.csv" if len(sys.argv) < 2 else sys.argv[1]
    output_dir = "logs" if len(sys.argv) < 3 else sys.argv[2]

    run_evaluation(csv_file, output_dir)
