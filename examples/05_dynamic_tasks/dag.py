from datetime import datetime

from airflow import DAG
from airflow.decorators import task


with DAG(
    dag_id="dynamic_tasks_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning", "dynamic-tasks"],
) as dag:

    @task
    def list_files() -> list[str]:
        return ["customers.csv", "orders.csv", "products.csv"]

    @task
    def process_file(file_name: str) -> str:
        print(f"Processing {file_name}")
        return f"processed_{file_name}"

    process_file.expand(file_name=list_files())
