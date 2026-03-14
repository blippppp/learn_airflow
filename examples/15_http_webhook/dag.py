from datetime import datetime
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import json


def process_users(**context):
    """Process the list of users fetched from the API."""
    users = context["ti"].xcom_pull(task_ids="fetch_users")
    print(f"Fetched {len(users)} users")
    # Return the list of user IDs for the next task
    return [user["id"] for user in users]


def fetch_posts_for_user(user_id, **context):
    """Fetch posts for a specific user ID."""
    import requests
    response = requests.get(f"https://jsonplaceholder.typicode.com/posts?userId={user_id}")
    posts = response.json()
    print(f"User {user_id} has {len(posts)} posts")
    return len(posts)


def summarize_results(**context):
    """Summarize the results from the mapped tasks."""
    # Get the list of post counts from the mapped tasks
    post_counts = context["ti"].xcom_pull(task_ids="fetch_posts_for_user")
    total_posts = sum(post_counts)
    print(f"Total posts across all users: {total_posts}")


with DAG(
    dag_id="http_webhook_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=["learning", "http", "api", "webhook"],
) as dag:
    # Task 1: Fetch list of users using SimpleHttpOperator
    fetch_users = SimpleHttpOperator(
        task_id="fetch_users",
        http_conn_id="jsonplaceholder_api",
        endpoint="/users",
        method="GET",
        response_filter=lambda response: json.loads(response.text),
        log_response=True,
    )

    # Task 2: Process the list of users to extract user IDs
    process_users_task = PythonOperator(
        task_id="process_users",
        python_callable=process_users,
    )

    # Task 3: Dynamically map over user IDs to fetch posts for each user
    fetch_posts_for_user = PythonOperator(
        task_id="fetch_posts_for_user",
        python_callable=fetch_posts_for_user,
    )

    # Task 4: Summarize the results
    summarize_task = PythonOperator(
        task_id="summarize_results",
        python_callable=summarize_results,
    )

    # Set up dependencies
    fetch_users >> process_users_task >> fetch_posts_for_user.expand(op_args=process_users_task.output) >> summarize_task
