from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator


def choose_path() -> str:
    return "even_day_task" if datetime.utcnow().day % 2 == 0 else "odd_day_task"


with DAG(
    dag_id="branching_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["learning", "branching"],
) as dag:
    start = EmptyOperator(task_id="start")
    branch = BranchPythonOperator(task_id="choose_path", python_callable=choose_path)
    even = EmptyOperator(task_id="even_day_task")
    odd = EmptyOperator(task_id="odd_day_task")
    end = EmptyOperator(task_id="end", trigger_rule="none_failed_min_one_success")
    start >> branch >> [even, odd] >> end
