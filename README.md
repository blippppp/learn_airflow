# Airflow Learning: Hands-On Apache Airflow Project

A practical repository for learning Apache Airflow by building and running real DAGs.

## What you'll learn

This repo teaches Airflow concepts incrementally through **10 runnable examples**:

1. Hello DAG and scheduling basics
2. Task dependencies
3. XCom data passing
4. Branching
5. Dynamic task mapping
6. Sensors
7. CSV ETL with Pandas
8. Database pipeline with Postgres
9. API pipeline
10. Data quality checks

Each example includes:

- A working DAG
- A focused README with concept explanation
- Step-by-step run instructions

---

## Repository layout

```text
airflow-learning/
├── README.md
├── docker-compose.yml
├── requirements.txt
├── dags/
├── examples/
│   ├── 01_hello_dag
│   ├── 02_task_dependencies
│   ├── 03_xcom
│   ├── 04_branching
│   ├── 05_dynamic_tasks
│   ├── 06_sensors
│   ├── 07_csv_etl
│   ├── 08_database_pipeline
│   ├── 09_api_pipeline
│   └── 10_data_quality
├── datasets/
└── docs/
```

---

## Prerequisites

- Python 3.10+
- Docker + Docker Compose (recommended path)
- `git`

---

## Option 1 (Recommended): Run with Docker

### 1) Clone and enter the repo

```bash
git clone <your-repo-url> airflow-learning
cd airflow-learning
```

### 2) Set Airflow UID (Linux only)

```bash
echo "AIRFLOW_UID=$(id -u)" > .env
```

On macOS/Windows, you can skip this and use:

```bash
echo "AIRFLOW_UID=50000" > .env
```

### 3) Initialize Airflow metadata DB

```bash
docker compose up airflow-init
```

### 4) Start Airflow services

```bash
docker compose up -d
```

### 5) Open Airflow UI

- URL: http://localhost:8080
- Username: `airflow`
- Password: `airflow`

### 6) Trigger DAGs

Enable a DAG in the UI and click **Trigger DAG**.

> DAGs are loaded directly from `examples/` in this project.

### 7) Stop services

```bash
docker compose down
```

---

## Option 2: Run in a local Python environment

### 1) Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

### 3) Set Airflow home and DAG folder

```bash
export AIRFLOW_HOME=$(pwd)/.airflow
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__CORE__DAGS_FOLDER=$(pwd)/examples
```

### 4) Initialize metadata DB

```bash
airflow db init
```

### 5) Create an admin user

```bash
airflow users create \
  --username airflow \
  --firstname Air \
  --lastname Flow \
  --role Admin \
  --email airflow@example.com \
  --password airflow
```

### 6) Start scheduler and webserver

In terminal 1:

```bash
airflow scheduler
```

In terminal 2:

```bash
airflow webserver --port 8080
```

Open http://localhost:8080 and trigger DAGs.

---

## Learning path

Follow examples in order:

1. `examples/01_hello_dag`
2. `examples/02_task_dependencies`
3. `examples/03_xcom`
4. `examples/04_branching`
5. `examples/05_dynamic_tasks`
6. `examples/06_sensors`
7. `examples/07_csv_etl`
8. `examples/08_database_pipeline`
9. `examples/09_api_pipeline`
10. `examples/10_data_quality`

See `docs/learning_path.md` for a suggested schedule.

---

## Backfill and retries quick demo

Use DAG `02_task_dependencies` to test retries and backfills:

```bash
airflow dags backfill task_dependencies_dag -s 2024-01-01 -e 2024-01-03
```

In this DAG, tasks include retry settings so you can inspect retry behavior in UI/logs.

---

## Troubleshooting

- If DAGs don't appear, verify `AIRFLOW__CORE__DAGS_FOLDER` points to `examples`.
- If Docker containers fail with permissions, ensure `AIRFLOW_UID` is set.
- If local install fails due to constraints, follow Apache Airflow's constraints docs for your Python version.

