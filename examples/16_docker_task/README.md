# 16 - Docker Task

Run tasks in isolated Docker containers using `DockerOperator`.

## Overview
This DAG demonstrates:
- Running a simple command in a Docker container
- Mounting volumes to access files from the host
- Using the Docker socket to communicate with the Docker daemon

## Prerequisites
- Docker daemon running and accessible via the Unix socket
- The `docker` provider package installed (already in `requirements.txt`)

## How it works
1. **check_file_exists**: PythonOperator that checks if the CSV file exists in the datasets directory
2. **run_in_docker**: DockerOperator that runs a simple Python command in a `python:3.11-slim` container
3. **count_rows_in_docker**: DockerOperator that:
   - Uses the same `python:3.11-slim` image
   - Mounts the host's `./datasets` directory into the container at `/opt/airflow/datasets`
   - Runs a script to count rows in the CSV file

## Important Notes
- The Docker socket (`/var/run/docker.sock`) is mounted into the Airflow containers to allow the DockerOperator to communicate with the Docker daemon
- This setup is **for learning purposes only** - in production, you should consider security implications of exposing the Docker socket
- The DockerOperator automatically removes the container after execution (`auto_remove=True`)

## Run
```bash
airflow dags trigger docker_task_dag
```

## View Logs
Check the task logs in the Airflow UI to see the output from the Docker containers.