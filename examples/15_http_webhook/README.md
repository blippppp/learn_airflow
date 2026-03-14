# 15 - HTTP Webhook Pipeline

Fetch data from a public REST API using `SimpleHttpOperator` and demonstrate dynamic task mapping.

## Overview
This DAG demonstrates:
- Fetching a list of users from a public API (`jsonplaceholder.typicode.com`)
- Extracting user IDs from the response
- Dynamically mapping a task to fetch posts for each user
- Summarizing the total number of posts across all users

## Create Airflow connection
- Conn Id: `jsonplaceholder_api`
- Type: `HTTP`
- Host: `https://jsonplaceholder.typicode.com`
- Leave other fields blank (no authentication needed for this public API)

## Run
```bash
airflow dags trigger http_webhook_dag
```

## Notes
- Uses the free, public JSONPlaceholder API for demonstration
- Shows how to use `SimpleHttpOperator` for GET requests with JSON response filtering
- Demonstrates dynamic task mapping with `.expand()` to process a list of items
- The API returns fake data suitable for testing and learning