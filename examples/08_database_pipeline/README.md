# 08 - Database Pipeline (Postgres)

Load transformed data into Postgres with `PostgresHook`.

## Create Airflow connection
- Conn Id: `airflow_db`
- Type: `Postgres`
- Host: `postgres` (Docker) or `localhost` (local)
- Schema: `airflow`
- Login/Password: `airflow` / `airflow`
- Port: `5432`

## Run
```bash
airflow dags trigger database_pipeline_dag
```
