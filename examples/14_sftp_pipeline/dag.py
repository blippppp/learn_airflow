import os
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.sftp.hooks.sftp import SFTPHook


DATASETS_DIR = Path(os.getenv("DATASETS_DIR", Path(__file__).resolve().parents[2] / "datasets"))
INPUT_FILE = DATASETS_DIR / "sales_cleaned.csv"
OUTPUT_FILE = DATASETS_DIR / "sales_downloaded_from_sftp.csv"


def extract() -> str:
    """Read the cleaned CSV file and return as JSON."""
    import pandas as pd
    df = pd.read_csv(INPUT_FILE)
    return df.to_json(orient="records")


def upload_to_sftp(**context) -> str:
    """Upload the CSV file to SFTP server."""
    hook = SFTPHook(ftp_conn_id="sftp_default")
    
    # Upload file
    hook.store_file(
        remotepath=f"/home/airflow/upload/sales_cleaned.csv",
        localpath=str(INPUT_FILE),
    )
    
    return f"sftp://{hook.conn.host}/home/airflow/upload/sales_cleaned.csv"


def list_sftp_files(**context) -> list:
    """List files in the SFTP directory to verify upload."""
    hook = SFTPHook(ftp_conn_id="sftp_default")
    return hook.list_directory("/home/airflow/upload")


def download_from_sftp(**context) -> None:
    """Download the file back from SFTP and verify."""
    hook = SFTPHook(ftp_conn_id="sftp_default")
    
    # Download file
    hook.retrieve_file(
        remotepath=f"/home/airflow/upload/sales_cleaned.csv",
        localpath=str(OUTPUT_FILE),
    )
    
    # Verify download
    if OUTPUT_FILE.exists():
        import pandas as pd
        df = pd.read_csv(OUTPUT_FILE)
        print(f"Downloaded {len(df)} rows from SFTP")
    else:
        raise FileNotFoundError(f"Failed to download file from SFTP")


# Import pandas inside the DAG to avoid serialization issues
import pandas as pd

with DAG(
    dag_id="sftp_pipeline_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning", "sftp", "file-transfer"],
) as dag:
    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    upload_task = PythonOperator(task_id="upload_to_sftp", python_callable=upload_to_sftp)
    list_task = PythonOperator(task_id="list_sftp_files", python_callable=list_sftp_files)
    download_task = PythonOperator(task_id="download_from_sftp", python_callable=download_from_sftp)
    
    extract_task >> upload_task >> list_task >> download_task