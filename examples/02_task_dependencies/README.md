# 02 - Task Dependencies, Retries, and Backfill

Demonstrates chaining with `>>`, retry settings, and `catchup=True`.

## Run
```bash
airflow dags trigger task_dependencies_dag
airflow dags backfill task_dependencies_dag -s 2024-01-01 -e 2024-01-03
```
