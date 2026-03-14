from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def say_hello() -> None:
    print("Hello from Apache Airflow learning project!")


with DAG(
    dag_id="hello_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["learning", "hello"],
) as dag:
    PythonOperator(task_id="say_hello", python_callable=say_hello)
