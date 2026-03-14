import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator


DATASETS_DIR = Path(os.getenv("DATASETS_DIR", Path(__file__).resolve().parents[2] / "datasets"))
INPUT_FILE = DATASETS_DIR / "sales.csv"
OUTPUT_FILE = DATASETS_DIR / "sales_cleaned.csv"


def extract() -> str:
    df = pd.read_csv(INPUT_FILE)
    return df.to_json(orient="records")


def transform(**context) -> str:
    df = pd.read_json(context["ti"].xcom_pull(task_ids="extract"))
    df["order_total"] = df["quantity"] * df["unit_price"]
    return df[df["quantity"] > 0].to_json(orient="records")


def load(**context) -> None:
    df = pd.read_json(context["ti"].xcom_pull(task_ids="transform"))
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved {len(df)} rows to {OUTPUT_FILE}")


with DAG(
    dag_id="csv_etl_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning", "etl", "pandas"],
) as dag:
    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    transform_task = PythonOperator(task_id="transform", python_callable=transform)
    load_task = PythonOperator(task_id="load", python_callable=load)
    extract_task >> transform_task >> load_task
