"""Example DAG that shows why you cannot create tasks in a for-loop using an XCom value.

This is *not* dynamic task mapping: it shows how to pull a list from an upstream task
and then iterate over it inside a single downstream task (similar to the CSV ETL example).

It also includes a commented-out snippet that would *fail* if you tried to do it at
DAG parse time (because the XCom value does not exist yet).
"""

from datetime import datetime

from airflow import DAG
from airflow.decorators import task


with DAG(
    dag_id="dynamic_tasks_xcom_loop_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning", "dynamic-tasks", "xcom"],
) as dag:

    @task
    def list_files() -> list[str]:
        # This value is returned via XCom at runtime
        return ["customers.csv", "orders.csv", "products.csv"]

    @task
    def process_all(**context) -> list[str]:
        # This is essentially what the CSV ETL example does: pull from XCom then loop.
        files = context["ti"].xcom_pull(task_ids="list_files")
        outputs: list[str] = []
        for f in files:
            print(f"Processing {f}")
            outputs.append(f"processed_{f}")
        return outputs

    # This works: `process_all` runs once, pulls the list, and loops inside the task.
    list_files() >> process_all()

    # ---
    # The following would NOT work if uncommented:
    #
    # files = list_files()  # <-- this is a Task object, not a list
    # for f in files:       # <-- Task objects are not iterable, and the list isn't available yet
    #     process_file(file_name=f)
    #
    # That code would raise at DAG-parse time. The list isn't available until runtime.
