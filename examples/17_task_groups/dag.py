from datetime import datetime
from airflow import DAG
from airflow.utils.task_group import TaskGroup
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator


def extract_csv(**context):
    print("Extracting data from CSV...")


def extract_api(**context):
    print("Extracting data from API...")


def clean_data(**context):
    print("Cleaning data...")


def enrich_data(**context):
    print("Enriching data...")


def load_to_db(**context):
    print("Loading data to database...")


def load_to_s3(**context):
    print("Loading data to S3...")


with DAG(
    dag_id="task_groups_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning", "taskgroup", "ui"],
) as dag:
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    # Extract group
    with TaskGroup("extract_group", tooltip="Extract tasks") as extract_group:
        extract_csv_task = PythonOperator(
            task_id="extract_csv",
            python_callable=extract_csv,
        )
        extract_api_task = PythonOperator(
            task_id="extract_api",
            python_callable=extract_api,
        )

    # Transform group
    with TaskGroup("transform_group", tooltip="Transform tasks") as transform_group:
        clean_data_task = PythonOperator(
            task_id="clean_data",
            python_callable=clean_data,
        )
        enrich_data_task = PythonOperator(
            task_id="enrich_data",
            python_callable=enrich_data,
        )

    # Load group
    with TaskGroup("load_group", tooltip="Load tasks") as load_group:
        load_to_db_task = PythonOperator(
            task_id="load_to_db",
            python_callable=load_to_db,
        )
        load_to_s3_task = PythonOperator(
            task_id="load_to_s3",
            python_callable=load_to_s3,
        )

    # Set up dependencies
    start >> extract_group >> transform_group >> load_group >> end