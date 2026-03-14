from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def produce_number() -> int:
    return 7


def multiply_number(**context) -> int:
    value = context["ti"].xcom_pull(task_ids="produce_number")
    return value * 6


def print_result(**context) -> None:
    result = context["ti"].xcom_pull(task_ids="multiply_number")
    print(f"Final result from XCom: {result}")


with DAG(
    dag_id="xcom_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning", "xcom"],
) as dag:
    t1 = PythonOperator(task_id="produce_number", python_callable=produce_number)
    t2 = PythonOperator(task_id="multiply_number", python_callable=multiply_number)
    t3 = PythonOperator(task_id="print_result", python_callable=print_result)
    t1 >> t2 >> t3
