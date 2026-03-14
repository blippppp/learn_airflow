from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.time_delta import TimeDeltaSensor


def after_wait() -> None:
    print("Sensor finished waiting")


with DAG(
    dag_id="sensors_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning", "sensors"],
) as dag:
    wait_30_seconds = TimeDeltaSensor(task_id="wait_30_seconds", delta=timedelta(seconds=30))
    continue_task = PythonOperator(task_id="continue_pipeline", python_callable=after_wait)
    wait_30_seconds >> continue_task
