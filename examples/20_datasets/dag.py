from datetime import datetime
from airflow import DAG
from airflow.datasets import Dataset
from airflow.operators.python import PythonOperator

# Define the dataset that we will produce and consume
DATASET = Dataset("file:///opt/airflow/datasets/sales_cleaned.csv")


def update_file(**context):
    """Update the file by running the CSV ETL process again (or just touch it)."""
    import os
    from pathlib import Path
    import pandas as pd

    datasets_dir = Path(os.getenv("DATASETS_DIR", Path(__file__).resolve().parents[2] / "datasets"))
    input_file = datasets_dir / "sales.csv"
    output_file = datasets_dir / "sales_cleaned.csv"

    # Run the ETL process to ensure the file is updated
    df = pd.read_csv(input_file)
    df["order_total"] = df["quantity"] * df["unit_price"]
    df = df[df["quantity"] > 0]
    df.to_csv(output_file, index=False)
    print(f"Updated {output_file} with {len(df)} rows")


def process_file(**context):
    """Process the file that has been updated by the producer."""
    import pandas as pd
    from pathlib import Path
    import os

    datasets_dir = Path(os.getenv("DATASETS_DIR", Path(__file__).resolve().parents[2] / "datasets"))
    input_file = datasets_dir / "sales_cleaned.csv"

    df = pd.read_csv(input_file)
    print(f"Processing {len(df)} rows from {input_file}")
    # Example processing: calculate total order value
    total_value = df["order_total"].sum()
    print(f"Total order value: {total_value:.2f}")


# Producer DAG: produces the dataset
with DAG(
    dag_id="producer_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,  # We'll trigger this manually or via another mechanism
    catchup=False,
    tags=["learning", "dataset", "producer"],
) as producer_dag:
    update_task = PythonOperator(
        task_id="update_file",
        python_callable=update_file,
        outlets=[DATASET],  # This task outlets the DATASET
    )


# Consumer DAG: consumes the dataset
with DAG(
    dag_id="consumer_dag",
    start_date=datetime(2024, 1, 1),
    schedule=[DATASET],  # This DAG is scheduled to run when the DATASET is updated
    catchup=False,
    tags=["learning", "dataset", "consumer"],
) as consumer_dag:
    process_task = PythonOperator(
        task_id="process_file",
        python_callable=process_file,
    )