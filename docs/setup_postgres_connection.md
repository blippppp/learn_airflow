# Setting up Postgres connection in Airflow

For `08_database_pipeline`, create a connection named `airflow_db`.

1. Open Airflow UI.
2. Go to **Admin → Connections**.
3. Add connection:
   - **Connection Id**: `airflow_db`
   - **Connection Type**: `Postgres`
   - **Host**: `postgres` (Docker) or `localhost` (local)
   - **Schema**: `airflow`
   - **Login**: `airflow`
   - **Password**: `airflow`
   - **Port**: `5432`
