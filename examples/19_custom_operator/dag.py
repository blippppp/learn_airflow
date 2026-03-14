import os
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

# Import the custom operator from the local package
from custom_operators.file_checksum_operator import FileChecksumOperator


DATASETS_DIR = Path(os.getenv("DATASETS_DIR", Path(__file__).resolve().parents[2] / "datasets"))
INPUT_FILE = DATASETS_DIR / "sales_cleaned.csv"


def use_checksum(**context):
    """Use the checksum computed by the custom operator."""
    checksum = context["ti"].xcom_pull(task_ids="compute_checksum")
    print(f"The checksum of the file is: {checksum}")


with DAG(
    dag_id="custom_operator_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning", "custom-operator", "extensibility"],
) as dag:
    # Task 1: Compute checksum using our custom operator
    compute_checksum = FileChecksumOperator(
        task_id="compute_checksum",
        file_path=str(INPUT_FILE),
        algorithm="md5",
    )

    # Task 2: Use the checksum result
    use_result = PythonOperator(
        task_id="use_checksum",
        python_callable=use_checksum,
    )

    # Set up dependencies
    compute_checksum >> use_result