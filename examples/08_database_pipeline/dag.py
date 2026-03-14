import os
from datetime import datetime
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook


DATASETS_DIR = Path(os.getenv("DATASETS_DIR", Path(__file__).resolve().parents[2] / "datasets"))
INPUT_FILE = DATASETS_DIR / "sales_cleaned.csv"


def create_table() -> None:
    hook = PostgresHook(postgres_conn_id="airflow_db")
    hook.run(
        """
        CREATE TABLE IF NOT EXISTS sales_metrics (
            order_id INT PRIMARY KEY,
            customer_name TEXT,
            quantity INT,
            unit_price NUMERIC,
            order_total NUMERIC
        );
        """
    )


def load_to_postgres() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Run csv_etl_dag first; missing {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)
    rows = [tuple(row) for row in df[["order_id", "customer_name", "quantity", "unit_price", "order_total"]].to_numpy()]

    hook = PostgresHook(postgres_conn_id="airflow_db")
    hook.insert_rows(
        table="sales_metrics",
        rows=rows,
        target_fields=["order_id", "customer_name", "quantity", "unit_price", "order_total"],
        replace=True,
    )


with DAG(
    dag_id="database_pipeline_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning", "database", "postgres"],
) as dag:
    create_table_task = PythonOperator(task_id="create_table", python_callable=create_table)
    load_task = PythonOperator(task_id="load_to_postgres", python_callable=load_to_postgres)
    create_table_task >> load_task
