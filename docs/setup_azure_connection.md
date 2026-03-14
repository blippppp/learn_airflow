# Setting up Azure Blob Storage connection in Airflow

For `13_azure_blob`, create a connection named `azure_blob_default`.

## Prerequisites
- An Azure Storage account
- A shared access signature (SAS) token or account key for authentication

## Steps
1. Go to the Azure Portal and navigate to your Storage Account
2. Under **Security + networking**, go to **Access keys** or **Shared access signature**
3. Copy the connection string or generate a SAS token
4. In Airflow UI:
   - Go to **Admin → Connections**
   - Add connection:
     - **Connection Id**: `azure_blob_default`
     - **Connection Type**: `Azure Blob Storage`
     - **Connection String**: `DefaultEndpointsProtocol=https;AccountName=<YOUR_ACCOUNT_NAME>;AccountKey=<YOUR_ACCOUNT_KEY>;EndpointSuffix=core.windows.net`

## Alternative: Using SAS Token
If you prefer to use a SAS token instead of the account key:
- **Connection Id**: `azure_blob_default`
- **Connection Type**: `Azure Blob Storage`
- **Login**: `<YOUR_ACCOUNT_NAME>`
- **Password**: `<SAS_TOKEN>` (without the leading `?`)
- **Extra (JSON)**:
  ```json
  {
    "sas_token": "<SAS_TOKEN>"
  }
  ```

## How it works
- The `WasbHook` uses this connection to authenticate with Azure Blob Storage
- The DAG creates a container named `airflow-data` (if it doesn't exist)
- Files are uploaded to the `sales/` folder within the container

## Notes
- The DAG uses the container name `airflow-data`. If it doesn't exist, the DAG will try to create it.
- Ensure your Azure account has permission to create containers and read/write blobs.
- Be aware of potential costs when running against a real Azure account.