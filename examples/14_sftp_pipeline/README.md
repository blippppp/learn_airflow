# 14 - SFTP Pipeline

Upload and download files to/from an SFTP server using `SFTPHook`.

## Overview
This DAG demonstrates:
- Reading a local CSV file
- Uploading it to an SFTP server
- Listing files in the remote directory to verify
- Downloading the file back locally

## Prerequisites
The `docker-compose.yml` includes an SFTP server service (`sftp-server`) that runs on port 2222.
The server is pre-configured with a user:
- Username: `airflow`
- Password: `airflow`

## Create Airflow connection
- Conn Id: `sftp_default`
- Type: `SFTP`
- Host: `sftp-server` (when running in Docker) or `localhost` (if using port forwarding)
- Port: `22` (inside Docker network) or `2222` (if connecting from host via localhost:2222)
- Login: `airflow`
- Password: `airflow`

## Run
```bash
airflow dags trigger sftp_pipeline_dag
```

## Notes
- The DAG uploads the file to `/home/airflow/upload/sales_cleaned.csv` in the SFTP container.
- The SFTP server in `docker-compose.yml` maps the container directory `/home/airflow/upload` to the host directory `./sftp-users`.
  You can find the uploaded file in `./sftp-users/sales_cleaned.csv` on your host machine.