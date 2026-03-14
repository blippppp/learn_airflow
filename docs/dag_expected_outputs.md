# DAG Expected Outputs Guide

This guide explains what to expect when each learning DAG runs in this project.

> Note: `dags/` is reserved for custom DAGs, while the lesson DAGs are loaded from `examples/` in this setup.

---

## 1) DAG Name
`hello_dag`

### Purpose
Demonstrates the smallest possible Airflow DAG: a single Python task that prints a message.

### DAG Structure
- `say_hello`

Dependency order:
- `say_hello` (single-task DAG, no upstream/downstream dependencies)

### Execution Flow
1. A DAG run starts.
2. Airflow schedules and executes `say_hello`.
3. The task prints a greeting and returns successfully.
4. The DAG run is marked `success`.

### Task Details
- **Task:** `say_hello`
  - **Operator:** `PythonOperator`
  - **What it does:** Calls `say_hello()` and prints a static greeting.
  - **Inputs/Outputs:**
    - Inputs: none
    - Output: `None` (no meaningful XCom payload)
  - **Retries/Special config:** no DAG-level retries configured.

### Expected Logs
- A print line similar to:
  - `Hello from Apache Airflow learning project!`

### Expected XCom Values
- No intentional XCom usage. (PythonOperator may auto-push `None` depending on Airflow version/config.)

### Expected Artifacts
- No files, tables, or external artifacts are created.

### How to Verify Success
- **Airflow UI:** DAG run and `say_hello` task are green (`success`).
- **Task logs:** Greeting message appears.
- **Filesystem/DB:** No output expected.

### Common Failure Scenarios
- Import/module errors if environment is broken.
- Scheduler/executor not running.
- Debug by checking scheduler/webserver logs and task log import traceback.

---

## 2) DAG Name
`task_dependencies_dag`

### Purpose
Demonstrates linear task dependencies (`extract >> transform >> load`) plus retries and backfill behavior (`catchup=True`).

### DAG Structure
- `extract`
- `transform`
- `load`

Dependency order:
- `extract` → `transform` → `load`

### Execution Flow
1. `extract` returns a small payload: `{"records": 100}`.
2. `transform` pulls that XCom, computes 95% cleaned rows (`95`), and returns `{"cleaned_records": 95}`.
3. `load` pulls transformed data and prints how many records were loaded.
4. DAG run completes successfully if all three tasks pass.

### Task Details
- **Task:** `extract`
  - **Operator:** `PythonOperator`
  - **What it does:** Emits a hard-coded dict with record count.
  - **Inputs/Outputs:** no input; outputs dict via XCom return value.
  - **Retries/Special config:** inherits DAG default retries.
- **Task:** `transform`
  - **Operator:** `PythonOperator`
  - **What it does:** Pulls `extract` XCom and computes cleaned count.
  - **Inputs/Outputs:** input from `extract` XCom; output dict via XCom.
  - **Retries/Special config:** inherits DAG default retries.
- **Task:** `load`
  - **Operator:** `PythonOperator`
  - **What it does:** Pulls `transform` XCom and prints load count.
  - **Inputs/Outputs:** input from `transform` XCom; output `None`.
  - **Retries/Special config:** inherits DAG default retries.

DAG-level retry config:
- `retries=2`
- `retry_delay=20 seconds`

### Expected Logs
- `load` task should print:
  - `Loaded 95 records`
- If an upstream task fails transiently, retry attempts should appear in logs.

### Expected XCom Values
- `extract` pushes: `{"records": 100}`
- `transform` pulls from `extract`, pushes: `{"cleaned_records": 95}`
- `load` pulls from `transform` and prints the value.

### Expected Artifacts
- No file or DB artifacts. This DAG is compute/log-focused.

### How to Verify Success
- **Airflow UI:** three tasks green in sequence.
- **Graph/Grid views:** clear linear dependency execution.
- **Task logs:** confirm XCom-driven value `95` appears in `load` logs.
- **XCom tab:** inspect return payloads for `extract` and `transform`.

### Common Failure Scenarios
- `KeyError` if expected XCom keys are missing.
- Type errors if payload shape changes.
- Retry exhaustion after 2 retries.
- Debug by inspecting upstream task return values and XCom entries.

---

## 3) DAG Name
`xcom_dag`

### Purpose
Demonstrates explicit value passing between tasks using XCom.

### DAG Structure
- `produce_number`
- `multiply_number`
- `print_result`

Dependency order:
- `produce_number` → `multiply_number` → `print_result`

### Execution Flow
1. `produce_number` returns `7`.
2. `multiply_number` pulls `7`, multiplies by `6`, returns `42`.
3. `print_result` pulls `42` and prints final message.

### Task Details
- **Task:** `produce_number`
  - **Operator:** `PythonOperator`
  - **What it does:** Returns integer `7`.
  - **Inputs/Outputs:** no inputs; XCom output `7`.
  - **Retries/Special config:** none explicit.
- **Task:** `multiply_number`
  - **Operator:** `PythonOperator`
  - **What it does:** Pulls prior XCom and returns multiplied value.
  - **Inputs/Outputs:** input `7`; output `42` via XCom.
  - **Retries/Special config:** none explicit.
- **Task:** `print_result`
  - **Operator:** `PythonOperator`
  - **What it does:** Pulls result and prints it.
  - **Inputs/Outputs:** input `42`; output `None`.
  - **Retries/Special config:** none explicit.

### Expected Logs
- `print_result` log should contain:
  - `Final result from XCom: 42`

### Expected XCom Values
- `produce_number`: `7`
- `multiply_number`: `42`
- `print_result`: pulls `42` from `multiply_number`

### Expected Artifacts
- No external artifacts.

### How to Verify Success
- **Airflow UI:** all 3 tasks succeed.
- **Task logs:** final log line includes `42`.
- **XCom tab:** verify integer values pushed by first two tasks.

### Common Failure Scenarios
- Wrong `task_ids` in `xcom_pull` leading to `None`.
- Arithmetic errors if upstream returns non-numeric type.
- Debug by checking XCom tab and upstream logs.

---

## 4) DAG Name
`branching_dag`

### Purpose
Demonstrates conditional branching with `BranchPythonOperator` and downstream join using a permissive trigger rule.

### DAG Structure
- `start`
- `choose_path`
- `even_day_task`
- `odd_day_task`
- `end`

Dependency order:
- `start` → `choose_path` → (`even_day_task` **or** `odd_day_task`) → `end`

### Execution Flow
1. `start` succeeds immediately.
2. `choose_path` checks current UTC day number.
3. It returns one task id:
   - even day: `even_day_task`
   - odd day: `odd_day_task`
4. Chosen branch runs; non-chosen branch is marked `skipped`.
5. `end` runs because trigger rule is `none_failed_min_one_success`.

### Task Details
- **Task:** `start`
  - **Operator:** `EmptyOperator`
  - **What it does:** placeholder start node.
  - **Inputs/Outputs:** none.
  - **Retries/Special config:** defaults.
- **Task:** `choose_path`
  - **Operator:** `BranchPythonOperator`
  - **What it does:** returns branch task id based on UTC day parity.
  - **Inputs/Outputs:** no explicit input; output task id string.
  - **Retries/Special config:** branch semantics (non-selected downstream skipped).
- **Task:** `even_day_task`
  - **Operator:** `EmptyOperator`
  - **What it does:** runs on even UTC day.
- **Task:** `odd_day_task`
  - **Operator:** `EmptyOperator`
  - **What it does:** runs on odd UTC day.
- **Task:** `end`
  - **Operator:** `EmptyOperator`
  - **What it does:** join/finalize node.
  - **Retries/Special config:** `trigger_rule="none_failed_min_one_success"`.

### Expected Logs
- `choose_path` logs the returned branch task id.
- One branch task is `success`, the other `skipped`.
- `end` should execute successfully when one branch succeeds.

### Expected XCom Values
- `choose_path` returns selected task id (stored as return XCom).

### Expected Artifacts
- No external artifacts.

### How to Verify Success
- **Airflow UI Graph:** one branch green, one yellow (`skipped`), `end` green.
- **Task Instance states:** confirm skip behavior is expected.
- **Logs:** branch decision visible in `choose_path` logs.

### Common Failure Scenarios
- Returning wrong task id in branch function causes downstream mismatch.
- Misconfigured trigger rule on `end` can cause unexpected skip.
- Debug by verifying branch return value and downstream task IDs.

---

## 5) DAG Name
`dynamic_tasks_dag`

### Purpose
Demonstrates dynamic task mapping using TaskFlow API (`@task` and `.expand`).

### DAG Structure
- `list_files`
- `process_file` (dynamically mapped task instances)

Dependency order:
- `list_files` → `process_file[file_name=customers.csv|orders.csv|products.csv]`

### Execution Flow
1. `list_files` returns three filenames.
2. Airflow creates three mapped `process_file` task instances.
3. Each mapped task prints its filename and returns processed filename.
4. DAG succeeds when all mapped tasks complete.

### Task Details
- **Task:** `list_files`
  - **Operator:** TaskFlow-decorated Python task (internally PythonOperator-like execution)
  - **What it does:** returns list of file names.
  - **Inputs/Outputs:** no inputs; output list via XComArg.
  - **Retries/Special config:** none explicit.
- **Task:** `process_file` (mapped)
  - **Operator:** TaskFlow mapped Python task
  - **What it does:** processes each input filename independently.
  - **Inputs/Outputs:** input single `file_name`; output `processed_<file_name>`.
  - **Retries/Special config:** dynamic expansion via `.expand(file_name=list_files())`.

### Expected Logs
- One log set per mapped index, each containing e.g.:
  - `Processing customers.csv`
  - `Processing orders.csv`
  - `Processing products.csv`

### Expected XCom Values
- `list_files` pushes list:
  - `["customers.csv", "orders.csv", "products.csv"]`
- Mapped `process_file` pushes per-index values:
  - `processed_customers.csv`, `processed_orders.csv`, `processed_products.csv`

### Expected Artifacts
- No filesystem artifacts; this is a mapping behavior example.

### How to Verify Success
- **Airflow UI Grid:** mapped task shows expanded instances.
- **Mapped task logs:** each file-specific processing message appears.
- **XCom:** inspect each mapped TI’s return value.

### Common Failure Scenarios
- Expansion input not a list/iterable.
- Serialization issues if non-JSON-serializable return values are introduced.
- Debug via mapped task index logs and XCom per map index.

---

## 6) DAG Name
`sensors_dag`

### Purpose
Demonstrates sensor behavior using a `TimeDeltaSensor` wait before continuing a pipeline.

### DAG Structure
- `wait_30_seconds`
- `continue_pipeline`

Dependency order:
- `wait_30_seconds` → `continue_pipeline`

### Execution Flow
1. `wait_30_seconds` starts and waits until 30 seconds have elapsed.
2. Once sensor condition is met, task succeeds.
3. `continue_pipeline` executes and prints completion message.

### Task Details
- **Task:** `wait_30_seconds`
  - **Operator:** `TimeDeltaSensor`
  - **What it does:** pauses progression for 30 seconds.
  - **Inputs/Outputs:** no data payload; temporal condition check.
  - **Retries/Special config:** `delta=30 seconds`.
- **Task:** `continue_pipeline`
  - **Operator:** `PythonOperator`
  - **What it does:** runs after sensor and prints message.
  - **Inputs/Outputs:** no meaningful input/output.

### Expected Logs
- Sensor logs periodic poking/wait behavior until condition met.
- Continue task logs:
  - `Sensor finished waiting`

### Expected XCom Values
- No intentional business XCom usage.

### Expected Artifacts
- No external artifacts.

### How to Verify Success
- **Airflow UI:** observe first task running for ~30 seconds before success.
- **Task logs:** sensor wait then completion message in second task.

### Common Failure Scenarios
- Executor slot pressure can delay sensor execution.
- If sensor mode/config changes, behavior may differ.
- Debug by checking sensor logs and worker availability.

---

## 7) DAG Name
`csv_etl_dag`

### Purpose
Demonstrates a pandas-based ETL pipeline from CSV input to cleaned CSV output.

### DAG Structure
- `extract`
- `transform`
- `load`

Dependency order:
- `extract` → `transform` → `load`

### Execution Flow
1. `extract` reads `datasets/sales.csv`, converts rows to JSON string, returns via XCom.
2. `transform` parses JSON, computes `order_total = quantity * unit_price`, filters `quantity > 0`, returns cleaned JSON.
3. `load` parses cleaned JSON and writes `datasets/sales_cleaned.csv`.
4. Task logs include saved row count and output path.

### Task Details
- **Task:** `extract`
  - **Operator:** `PythonOperator`
  - **What it does:** reads source CSV with pandas.
  - **Inputs/Outputs:** input `sales.csv`; output JSON records string.
  - **Retries/Special config:** none explicit.
- **Task:** `transform`
  - **Operator:** `PythonOperator`
  - **What it does:** computes derived column and filters rows.
  - **Inputs/Outputs:** input extract JSON; output transformed JSON.
- **Task:** `load`
  - **Operator:** `PythonOperator`
  - **What it does:** writes cleaned dataframe to CSV.
  - **Inputs/Outputs:** input transformed JSON; output file `sales_cleaned.csv`.
  - **Retries/Special config:** ensures output directory exists.

### Expected Logs
- `load` task prints:
  - `Saved <N> rows to <...>/sales_cleaned.csv`
- Upstream logs may include pandas read/parse execution details.

### Expected XCom Values
- `extract`: JSON array of input records.
- `transform`: JSON array including `order_total` and only rows where `quantity > 0`.
- `load`: pulls transformed JSON and writes to disk.

### Expected Artifacts
- **Filesystem file:** `datasets/sales_cleaned.csv`
- File should include columns from source plus `order_total`.

### How to Verify Success
- **Airflow UI:** all three tasks green.
- **Task logs:** `Saved <N> rows ...` line in `load`.
- **Filesystem:** confirm `datasets/sales_cleaned.csv` exists and is non-empty.
- **Data check:** inspect CSV headers/rows for `order_total` and positive quantities.

### Common Failure Scenarios
- Missing source file `datasets/sales.csv`.
- Pandas parse/serialization issues.
- Permission issues writing output file.
- Debug by verifying input file path, `DATASETS_DIR`, and stack traces.

---

## 8) DAG Name
`database_pipeline_dag`

### Purpose
Demonstrates loading cleaned CSV data into PostgreSQL using `PostgresHook`.

### DAG Structure
- `create_table`
- `load_to_postgres`

Dependency order:
- `create_table` → `load_to_postgres`

### Execution Flow
1. `create_table` connects via `airflow_db` connection and creates `sales_metrics` table if absent.
2. `load_to_postgres` checks for `datasets/sales_cleaned.csv`.
3. It reads the CSV and inserts/replaces rows into `sales_metrics`.
4. DAG succeeds after table creation and load complete.

### Task Details
- **Task:** `create_table`
  - **Operator:** `PythonOperator`
  - **What it does:** runs `CREATE TABLE IF NOT EXISTS sales_metrics (...)` via `PostgresHook.run`.
  - **Inputs/Outputs:** DB connection input; output is side-effect (table creation).
  - **Retries/Special config:** relies on connection `postgres_conn_id="airflow_db"`.
- **Task:** `load_to_postgres`
  - **Operator:** `PythonOperator`
  - **What it does:** reads cleaned CSV and inserts rows.
  - **Inputs/Outputs:** input CSV file; output side-effect in Postgres table.
  - **Retries/Special config:** raises `FileNotFoundError` if cleaned CSV is missing; `insert_rows(..., replace=True)` for upsert-like replacement by PK.

### Expected Logs
- Successful DB connection and SQL execution logs.
- If prerequisite file is missing, clear error:
  - `Run csv_etl_dag first; missing .../sales_cleaned.csv`

### Expected XCom Values
- No intentional XCom business payloads.

### Expected Artifacts
- **Database table:** `sales_metrics`
- **Database rows:** loaded from `sales_cleaned.csv` with columns:
  - `order_id`, `customer_name`, `quantity`, `unit_price`, `order_total`

### How to Verify Success
- **Airflow UI:** both tasks green.
- **Task logs:** no DB exceptions; successful inserts.
- **Database:** query `SELECT COUNT(*) FROM sales_metrics;` and inspect sample rows.
- **Prereq:** confirm `csv_etl_dag` ran and output CSV exists.

### Common Failure Scenarios
- Missing Airflow connection `airflow_db` or wrong credentials.
- Missing prerequisite CSV.
- DB connectivity/network issues.
- PK conflicts/type issues if source data malformed.
- Debug by checking connection config in Airflow, task tracebacks, and DB logs.

---

## 9) DAG Name
`api_pipeline_dag`

### Purpose
Demonstrates pulling data from an external API and summarizing it.

### DAG Structure
- `fetch_posts`
- `summarize_posts`

Dependency order:
- `fetch_posts` → `summarize_posts`

### Execution Flow
1. `fetch_posts` requests JSONPlaceholder posts endpoint.
2. It validates HTTP status and returns first 5 posts.
3. `summarize_posts` pulls posts, computes count and title lengths, prints/returns summary.
4. DAG run is successful when both tasks pass.

### Task Details
- **Task:** `fetch_posts`
  - **Operator:** `PythonOperator`
  - **What it does:** HTTP GET with timeout=20s, raises on non-2xx, slices first five posts.
  - **Inputs/Outputs:** input external API; output list of 5 post dicts.
  - **Retries/Special config:** timeout configured in `requests.get`.
- **Task:** `summarize_posts`
  - **Operator:** `PythonOperator`
  - **What it does:** computes summary dict and prints it.
  - **Inputs/Outputs:** input list of posts from XCom; output summary dict.

### Expected Logs
- `summarize_posts` prints dict similar to:
  - `{'count': 5, 'title_lengths': [..five ints..]}`

### Expected XCom Values
- `fetch_posts`: list containing 5 post objects.
- `summarize_posts`: summary dict with keys `count` and `title_lengths`.

### Expected Artifacts
- No files/tables created; external effect is outbound API call.

### How to Verify Success
- **Airflow UI:** two green tasks.
- **Logs:** summary dict appears in `summarize_posts`.
- **XCom:** inspect API payload and computed summary.

### Common Failure Scenarios
- No internet / DNS / TLS failures.
- HTTP errors from endpoint.
- API schema drift (missing `title` field).
- Debug via request exception in logs and by re-running task.

---

## 10) DAG Name
`data_quality_dag`

### Purpose
Demonstrates sequential data quality checks on cleaned CSV output.

### DAG Structure
- `check_not_empty`
- `check_non_negative_totals`
- `check_unique_order_id`

Dependency order:
- `check_not_empty` → `check_non_negative_totals` → `check_unique_order_id`

### Execution Flow
1. `check_not_empty` verifies cleaned CSV exists and has rows.
2. `check_non_negative_totals` fails if any `order_total < 0`.
3. `check_unique_order_id` fails if `order_id` has duplicates.
4. DAG succeeds only if all checks pass.

### Task Details
- **Task:** `check_not_empty`
  - **Operator:** `PythonOperator`
  - **What it does:** validates file existence and non-empty dataset.
  - **Inputs/Outputs:** input `sales_cleaned.csv`; output pass/fail only.
  - **Retries/Special config:** raises explicit errors for missing/empty data.
- **Task:** `check_non_negative_totals`
  - **Operator:** `PythonOperator`
  - **What it does:** queries for negative totals and fails if present.
  - **Inputs/Outputs:** input cleaned CSV; output pass/fail only.
- **Task:** `check_unique_order_id`
  - **Operator:** `PythonOperator`
  - **What it does:** checks uniqueness of `order_id`.
  - **Inputs/Outputs:** input cleaned CSV; output pass/fail only.

### Expected Logs
- On success: no exception traces, tasks complete quietly.
- On failure: explicit error messages, e.g.:
  - `Run csv_etl_dag first; missing .../sales_cleaned.csv`
  - `Data quality failed: empty dataset`
  - `Data quality failed: negative totals found`
  - `Data quality failed: duplicate order_id values`

### Expected XCom Values
- No intentional XCom business values.

### Expected Artifacts
- No new artifacts; validates existing `sales_cleaned.csv` quality.

### How to Verify Success
- **Airflow UI:** all three checks green.
- **Task logs:** absence of raised exceptions.
- **Filesystem/data:** inspect `sales_cleaned.csv` for non-empty rows, non-negative totals, unique IDs.

### Common Failure Scenarios
- Missing prerequisite output from `csv_etl_dag`.
- Bad transformation logic producing negative totals or duplicates.
- Corrupted CSV format.
- Debug by opening the CSV directly and reproducing failing check locally.

---

## Quick Validation Checklist (All DAGs)
For any DAG in this learning project, verify in this order:
1. DAG run state is `success` in Airflow UI.
2. Every task instance state is expected (`success` / intentional `skipped` for branching).
3. Logs contain expected messages listed above.
4. XCom entries match expected payloads (where applicable).
5. External artifacts (CSV files, Postgres table data) exist and contain expected data.
