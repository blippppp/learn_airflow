# dags/

This folder is reserved for your custom DAGs.

In this learning project, the lesson DAGs are loaded from `examples/` by setting:

- `AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/examples` (Docker)
- `AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/examples` (local)

You can still add any additional DAGs here and change your DAG folder setting if needed.
