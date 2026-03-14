# 17 - Task Groups

Organize tasks in the Airflow UI using `TaskGroup`.

## Overview
This DAG demonstrates:
- Using `TaskGroup` to visually group related tasks in the Airflow UI
- Setting up dependencies between task groups
- Nesting tasks within groups

## Structure
The DAG has three main groups:
1. **extract_group**: Contains tasks for extracting data from CSV and API
2. **transform_group**: Contains tasks for cleaning and enriching data
3. **load_group**: Contains tasks for loading data to database and S3

## How it works
- Each group is defined using a `with TaskGroup(...)` context manager
- Tasks inside the group are indented under the context manager
- Dependencies are set between groups (not individual tasks) using the group objects
- In the Airflow UI, you can collapse/expand each group to hide/show its tasks

## Run
```bash
airflow dags trigger task_groups_dag
```

## View in Airflow UI
1. Open the DAG view for `task_groups_dag`
2. You'll see three colored boxes representing the task groups
3. Click on a group to expand and see the tasks inside
4. The dependencies between groups are shown as arrows between the group boxes