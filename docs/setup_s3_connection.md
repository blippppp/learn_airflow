# Setting up S3 connection in Airflow (MinIO)

For `11_s3_pipeline`, create a connection named `minio_s3`.

1. Open Airflow UI.
2. Go to **Admin → Connections**.
3. Add connection:
   - **Connection Id**: `minio_s3`
   - **Connection Type**: `Amazon Web Services`
   - **Extra (JSON)**:
     ```json
     {
       "endpoint_url": "http://minio:9000",
       "aws_access_key_id": "minioadmin",
       "aws_secret_access_key": "minioadmin"
     }
     ```

## How it works
- The MinIO service is running in Docker on port 9000 (API) and 9001 (Console)
- The `endpoint_url` points to the MinIO service within the Docker network
- The credentials `minioadmin`/`minioadmin` are the default MinIO credentials
- The DAG uses this connection to upload/download files to/from the `airflow-data` bucket

## Verify in MinIO Console
1. Open http://localhost:9001 in your browser
2. Login with:
   - Username: `minioadmin`
   - Password: `minioadmin`
3. Browse to the `airflow-data` bucket and `sales` folder to see files uploaded by the DAG.