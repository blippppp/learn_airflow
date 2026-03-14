from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator


def extract() -> dict:
    return {"records": 100}


def transform(**context) -> dict:
    payload = context["ti"].xcom_pull(task_ids="extract")
    return {"cleaned_records": int(payload["records"] * 0.95)}


def load(**context) -> None:
    cleaned = context["ti"].xcom_pull(task_ids="transform")["cleaned_records"]
    print(f"Loaded {cleaned} records")


with DAG(
    dag_id="task_dependencies_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=True,
    default_args={"retries": 2, "retry_delay": timedelta(seconds=20)},
    tags=["learning", "dependencies", "retries", "backfill"],
) as dag:
    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    transform_task = PythonOperator(task_id="transform", python_callable=transform)
    load_task = PythonOperator(task_id="load", python_callable=load)
    extract_task >> transform_task >> load_task
