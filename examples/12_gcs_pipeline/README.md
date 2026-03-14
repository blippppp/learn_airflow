# 12 - GCS Pipeline

Upload and download files to/from Google Cloud Storage using `GCSHook`.

## Overview
This DAG demonstrates:
- Reading a local CSV file
- Uploading it to a Google Cloud Storage bucket
- Downloading the file back locally

## Prerequisites
- A Google Cloud Platform project
- A service account with `Storage Admin` role (or at least `Storage Object Admin`)
- A GCS bucket (e.g., `airflow-learning-bucket`)

## Create Airflow connection
- Conn Id: `google_cloud_default`
- Type: `Google Cloud`
- Keyfile Path: Path to the service account JSON key file (or upload the JSON and use the "Keyfile JSON" option)

## Run
```bash
airflow dags trigger gcs_pipeline_dag
```

## Notes
- The DAG uses the bucket name `airflow-learning-bucket`. Change it in the DAG if your bucket has a different name.
- Ensure the service account has permission to read/write to the specified bucket.