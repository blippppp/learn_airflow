# 13 - Azure Blob Storage Pipeline

Upload and download files to/from Azure Blob Storage using `WasbHook`.

## Overview
This DAG demonstrates:
- Reading a local CSV file
- Creating a blob container (if it doesn't exist)
- Uploading the file to Azure Blob Storage
- Downloading the file back locally

## Prerequisites
- An Azure Storage account
- A blob container (the DAG will attempt to create one named `airflow-data`)
- Shared Access Signature (SAS) token or account key for authentication

## Create Airflow connection
- Conn Id: `azure_blob_default`
- Type: `Azure Blob Storage`
- Either:
  - **Connection String**: `DefaultEndpointsProtocol=https;AccountName=<YOUR_ACCOUNT_NAME>;AccountKey=<YOUR_ACCOUNT_KEY>;EndpointSuffix=core.windows.net`
  - **SAS Token**: 
    - Login: `<YOUR_ACCOUNT_NAME>`
    - Password: `<SAS_TOKEN>` (without the leading `?`)
    - Extra (JSON): `{"sas_token": "<SAS_TOKEN>"}`

## Run
```bash
airflow dags trigger azure_blob_pipeline_dag
```

## Notes
- The DAG uses the container name `airflow-data`. If it doesn't exist, the DAG will try to create it.
- Ensure your Azure account has permission to create containers and read/write blobs.