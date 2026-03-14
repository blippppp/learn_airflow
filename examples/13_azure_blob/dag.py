import os
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.microsoft.azure.hooks.wasb import WasbHook


DATASETS_DIR = Path(os.getenv("DATASETS_DIR", Path(__file__).resolve().parents[2] / "datasets"))
INPUT_FILE = DATASETS_DIR / "sales_cleaned.csv"
OUTPUT_FILE = DATASETS_DIR / "sales_downloaded_from_azure.csv"


def extract() -> str:
    """Read the cleaned CSV file and return as JSON."""
    import pandas as pd
    df = pd.read_csv(INPUT_FILE)
    return df.to_json(orient="records")


def create_container(**context) -> None:
    """Create a blob container if it doesn't exist."""
    hook = WasbHook(wasb_conn_id="azure_blob_default")
    container_name = "airflow-data"
    if not hook.check_for_container(container_name):
        hook.create_container(container_name)


def upload_to_azure(**context) -> str:
    """Upload the CSV file to Azure Blob Storage."""
    hook = WasbHook(wasb_conn_id="azure_blob_default")
    container_name = "airflow-data"
    blob_name = "sales/sales_cleaned.csv"
    
    hook.load_file(
        file_path=str(INPUT_FILE),
        container_name=container_name,
        blob_name=blob_name,
        overwrite=True,
    )
    
    return f"wasb://{container_name}@{hook.account_name}.blob.core.windows.net/{blob_name}"


def download_from_azure(**context) -> None:
    """Download the file back from Azure Blob Storage and verify."""
    hook = WasbHook(wasb_conn_id="azure_blob_default")
    container_name = "airflow-data"
    blob_name = "sales/sales_cleaned.csv"
    
    hook.get_file(
        file_path=str(OUTPUT_FILE),
        container_name=container_name,
        blob_name=blob_name,
    )
    
    # Verify download
    if OUTPUT_FILE.exists():
        import pandas as pd
        df = pd.read_csv(OUTPUT_FILE)
        print(f"Downloaded {len(df)} rows from Azure Blob Storage")
    else:
        raise FileNotFoundError(f"Failed to download file from Azure Blob Storage")


# Import pandas inside the DAG to avoid serialization issues
import pandas as pd

with DAG(
    dag_id="azure_blob_pipeline_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning", "azure", "blob-storage", "cloud-storage"],
) as dag:
    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    create_container_task = PythonOperator(task_id="create_container", python_callable=create_container)
    upload_task = PythonOperator(task_id="upload_to_azure", python_callable=upload_to_azure)
    download_task = PythonOperator(task_id="download_from_azure", python_callable=download_from_azure)
    
    extract_task >> create_container_task >> upload_task >> download_task