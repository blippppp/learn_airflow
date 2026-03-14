# Setting up GCS connection in Airflow

For `12_gcs_pipeline`, create a connection named `google_cloud_default`.

## Prerequisites
- A Google Cloud Platform project
- A service account with `Storage Admin` role (or at least `Storage Object Admin`)
- A GCS bucket (the DAG uses `airflow-learning-bucket` by default)

## Steps
1. Create a service account in GCP Console
2. Grant it the `Storage Admin` role (or more restrictive permissions if preferred)
3. Download the service account key as a JSON file
4. In Airflow UI:
   - Go to **Admin → Connections**
   - Add connection:
     - **Connection Id**: `google_cloud_default`
     - **Connection Type**: `Google Cloud`
     - **Keyfile Path**: Path to the service account JSON key file
       (Alternatively, use "Keyfile JSON" and paste the entire JSON content)

## How it works
- The `GCSHook` uses this connection to authenticate with Google Cloud Storage
- The DAG uploads/downloads files to/from the specified bucket
- Make sure the service account has permission to read/write to the bucket used in the DAG

## Notes
- The DAG uses bucket name `airflow-learning-bucket` - change it in the DAG if your bucket has a different name
- Ensure the bucket exists before running the DAG, or add a task to create it