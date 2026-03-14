import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator


DATASETS_DIR = Path(os.getenv("DATASETS_DIR", Path(__file__).resolve().parents[2] / "datasets"))
INPUT_FILE = DATASETS_DIR / "sales_cleaned.csv"


def check_not_empty() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Run csv_etl_dag first; missing {INPUT_FILE}")
    if pd.read_csv(INPUT_FILE).empty:
        raise ValueError("Data quality failed: empty dataset")


def check_non_negative_totals() -> None:
    bad_rows = pd.read_csv(INPUT_FILE).query("order_total < 0")
    if not bad_rows.empty:
        raise ValueError("Data quality failed: negative totals found")


def check_unique_order_id() -> None:
    df = pd.read_csv(INPUT_FILE)
    if not df["order_id"].is_unique:
        raise ValueError("Data quality failed: duplicate order_id values")


with DAG(
    dag_id="data_quality_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning", "data-quality"],
) as dag:
    t1 = PythonOperator(task_id="check_not_empty", python_callable=check_not_empty)
    t2 = PythonOperator(task_id="check_non_negative_totals", python_callable=check_non_negative_totals)
    t3 = PythonOperator(task_id="check_unique_order_id", python_callable=check_unique_order_id)
    t1 >> t2 >> t3
