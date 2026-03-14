import os
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook


DATASETS_DIR = Path(os.getenv("DATASETS_DIR", Path(__file__).resolve().parents[2] / "datasets"))
INPUT_FILE = DATASETS_DIR / "sales_cleaned.csv"
OUTPUT_FILE = DATASETS_DIR / "sales_downloaded_from_gcs.csv"


def extract() -> str:
    """Read the cleaned CSV file and return as JSON."""
    import pandas as pd
    df = pd.read_csv(INPUT_FILE)
    return df.to_json(orient="records")


def upload_to_gcs(**context) -> str:
    """Upload the CSV file to GCS."""
    hook = GCSHook(gcp_conn_id="google_cloud_default")
    
    # Upload file
    hook.upload(
        bucket_name="airflow-learning-bucket",
        object_name="sales/sales_cleaned.csv",
        filename=str(INPUT_FILE),
    )
    
    return f"gs://airflow-learning-bucket/sales/sales_cleaned.csv"


def download_from_gcs(**context) -> None:
    """Download the file back from GCS and verify."""
    hook = GCSHook(gcp_conn_id="google_cloud_default")
    
    # Download file
    hook.download(
        bucket_name="airflow-learning-bucket",
        object_name="sales/sales_cleaned.csv",
        filename=str(OUTPUT_FILE),
    )
    
    # Verify download
    if OUTPUT_FILE.exists():
        import pandas as pd
        df = pd.read_csv(OUTPUT_FILE)
        print(f"Downloaded {len(df)} rows from GCS")
    else:
        raise FileNotFoundError(f"Failed to download file from GCS")


# Import pandas inside the DAG to avoid serialization issues
import pandas as pd

with DAG(
    dag_id="gcs_pipeline_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning", "gcs", "google-cloud", "cloud-storage"],
) as dag:
    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    upload_task = PythonOperator(task_id="upload_to_gcs", python_callable=upload_to_gcs)
    download_task = PythonOperator(task_id="download_from_gcs", python_callable=download_from_gcs)
    
    extract_task >> upload_task >> download_task