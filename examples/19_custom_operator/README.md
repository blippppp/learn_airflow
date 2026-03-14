# 19 - Custom Operator

Create a custom Airflow operator by extending `BaseOperator`.

## Overview
This DAG demonstrates:
- Creating a custom operator (`FileChecksumOperator`) that computes the MD5 or SHA256 checksum of a file
- Using the custom operator in a DAG
- How to push results to XCom for use by downstream tasks

## Custom Operator: FileChecksumOperator
- Inherits from `airflow.models.BaseOperator`
- Implements the `execute` method to compute the checksum
- Uses `@apply_defaults` decorator to handle default arguments
- Pushes the checksum result to XCom so it can be used by downstream tasks

## How it works
1. **compute_checksum**: An instance of `FileChecksumOperator` that computes the MD5 checksum of `sales_cleaned.csv`
2. **use_checksum**: A PythonOperator that retrieves the checksum from XCom and prints it

## To create your own custom operator
1. Create a class that inherits from `BaseOperator`
2. Implement the `__init__` method (consider using `@apply_defaults`)
3. Implement the `execute` method where the main logic resides
4. Optionally, push results to XCom using `return` or `xcom_push`

## Run
```bash
airflow dags trigger custom_operator_dag
```

## View Results
Check the logs for the `use_checksum` task to see the checksum printed.