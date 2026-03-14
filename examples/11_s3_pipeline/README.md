# 11 - S3 Pipeline (MinIO)

Upload and download files to/from S3 using `S3Hook` with a local MinIO server.

## Overview
This DAG demonstrates:
- Reading a local CSV file
- Uploading it to an S3-compatible service (MinIO)
- Listing objects in the bucket to verify
- Downloading the file back locally

## Create Airflow connection
- Conn Id: `minio_s3`
- Type: `Amazon Web Services`
- Extra (JSON):
  ```json
  {
    "endpoint_url": "http://minio:9000",
    "aws_access_key_id": "minioadmin",
    "aws_secret_access_key": "minioadmin"
  }
  ```

## Run
```bash
airflow dags trigger s3_pipeline_dag
```

## Verify in MinIO Console
1. Open http://localhost:9001 in your browser
2. Login with:
   - Username: `minioadmin`
   - Password: `minioadmin`
3. Browse to the `airflow-data` bucket and `sales` folder to see the uploaded file.