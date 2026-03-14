# 20 - Dataset-Driven Scheduling

Use Airflow's `Dataset` feature for data-aware scheduling (Airflow 2.4+).

## Overview
This example consists of two DAGs that demonstrate dataset-driven scheduling:
- **producer_dag**: Updates a file and outlets a `Dataset`
- **consumer_dag**: Is scheduled to run when the `Dataset` is updated

## How it works
1. **producer_dag**:
   - Runs the CSV ETL process to update `sales_cleaned.csv`
   - Uses `outlets=[DATASET]` to indicate that this task updates the dataset

2. **consumer_dag**:
   - Has `schedule=[DATASET]` which means it will be triggered automatically when the dataset is updated
   - Processes the updated file (calculates total order value in this example)

## Key concept
- Before Airflow 2.4, you would need to use sensors or external triggers to react to data updates
- With `Dataset`, you can declare that a task produces/consumes a dataset, and Airflow will automatically schedule dependent DAGs when datasets are updated
- The dataset URI (`file:///opt/airflow/datasets/sales_cleaned.csv`) is a logical identifier - it doesn't need to be a real URL

## Run
```bash
# First, trigger the producer DAG to create/update the dataset
airflow dags trigger producer_dag

# Then, you should see the consumer DAG get triggered automatically
# You can also trigger it manually to test:
airflow dags trigger consumer_dag
```

## View in Airflow UI
1. In the DAGs view, you'll see both `producer_dag` and `consumer_dag`
2. After running `producer_dag`, check the `consumer_dag` - it should show as triggered by a dataset update
3. In the graph view, you can see the dataset dependency between the DAGs