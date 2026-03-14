from datetime import datetime

from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator


def choose_path() -> list[str]:
    # Example: route to one of three paths based on the weekday,
    # while always running an "always" task.
    # - Mon/Tue -> "early_week"
    # - Wed/Thu -> "mid_week"
    # - Fri/Sat/Sun -> "late_week"
    # Always run "always_task" regardless of branch decision.
    weekday = datetime.utcnow().weekday()  # Mon=0 .. Sun=6

    always = ["always_task"]
    if weekday <= 1:
        return always + ["early_week_task"]
    if weekday <= 3:
        return always + ["mid_week_task"]
    return always + ["late_week_task"]


with DAG(
    dag_id="branching_dag",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["learning", "branching"],
) as dag:
    start = EmptyOperator(task_id="start")
    branch = BranchPythonOperator(task_id="choose_path", python_callable=choose_path)
    early_week = EmptyOperator(task_id="early_week_task")
    mid_week = EmptyOperator(task_id="mid_week_task")
    late_week = EmptyOperator(task_id="late_week_task")
    always = EmptyOperator(task_id="always_task")
    end = EmptyOperator(task_id="end", trigger_rule="none_failed_min_one_success")

    # Include `always` as a downstream task of the branch operator so it can be chosen
    # (BranchPythonOperator only allows task_ids that are downstream of it).
    start >> branch >> [early_week, mid_week, late_week, always] >> end
