from datetime import datetime

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator


def fetch_posts() -> list[dict]:
    response = requests.get("https://jsonplaceholder.typicode.com/posts", timeout=20)
    response.raise_for_status()
    return response.json()[:5]


def summarize_posts(**context) -> dict:
    posts = context["ti"].xcom_pull(task_ids="fetch_posts")
    summary = {"count": len(posts), "title_lengths": [len(p["title"]) for p in posts]}
    print(summary)
    return summary


with DAG(
    dag_id="api_pipeline_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning", "api"],
) as dag:
    fetch_task = PythonOperator(task_id="fetch_posts", python_callable=fetch_posts)
    summarize_task = PythonOperator(task_id="summarize_posts", python_callable=summarize_posts)
    fetch_task >> summarize_task
