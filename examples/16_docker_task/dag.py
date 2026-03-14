from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount


def check_file_exists(**context):
    """Check if the cleaned CSV file exists."""
    import os
    from pathlib import Path
    
    datasets_dir = Path(os.getenv("DATASETS_DIR", Path(__file__).resolve().parents[2] / "datasets"))
    input_file = datasets_dir / "sales_cleaned.csv"
    
    if input_file.exists():
        print(f"File {input_file} exists")
        return True
    else:
        print(f"File {input_file} does not exist")
        return False


def count_csv_rows(**context):
    """Count rows in the CSV file."""
    import pandas as pd
    from pathlib import Path
    import os
    
    datasets_dir = Path(os.getenv("DATASETS_DIR", Path(__file__).resolve().parents[2] / "datasets"))
    input_file = datasets_dir / "sales_cleaned.csv"
    
    df = pd.read_csv(input_file)
    row_count = len(df)
    print(f"CSV file has {row_count} rows")
    return row_count


with DAG(
    dag_id="docker_task_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning", "docker", "container"],
) as dag:
    # Task 1: Check if file exists (runs in Airflow worker)
    check_file = PythonOperator(
        task_id="check_file_exists",
        python_callable=check_file_exists,
    )

    # Task 2: Run a simple Python script in a Docker container
    run_in_docker = DockerOperator(
        task_id="run_in_docker",
        image="python:3.11-slim",
        api_version="auto",
        auto_remove=True,
        command="python -c \"print('Hello from Docker container!')\"",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
    )

    # Task 3: Count CSV rows in a Docker container with volume mount
    count_in_docker = DockerOperator(
        task_id="count_rows_in_docker",
        image="python:3.11-slim",
        api_version="auto",
        auto_remove=True,
        command="python -c \"import pandas as pd; df = pd.read_csv('/opt/airflow/datasets/sales_cleaned.csv'); print(f'Row count: {len(df)}')\"",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=[
            Mount(source="/opt/airflow/datasets", target="/opt/airflow/datasets", type="bind")
        ],
    )

    # Set up dependencies
    check_file >> run_in_docker >> count_in_docker