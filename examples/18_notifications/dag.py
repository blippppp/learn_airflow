from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.email import send_email


def failing_task(**context):
    """A task that always fails to trigger alerts."""
    raise ValueError("This task is designed to fail for demonstration purposes.")


def on_failure_callback(context):
    """Callback function that is executed when a task fails."""
    task_instance = context['task_instance']
    exception = context.get('exception')
    print(f"Task {task_instance.task_id} failed. Exception: {exception}")
    # In a real scenario, you might send a notification to a monitoring system here.


def send_success_email(**context):
    """Send an email on success (example)."""
    # This is just an example; you would need to configure email settings in airflow.cfg
    # or use the EmailOperator for a more integrated approach.
    send_email(
        to='airflow@example.com',
        subject='Airflow Success: notifications_dag',
        html_content='<p>The notifications_dag has completed successfully.</p>'
    )


with DAG(
    dag_id="notifications_dag",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    on_failure_callback=on_failure_callback,  # Set a DAG-level failure callback
    tags=["learning", "notifications", "alerts"],
) as dag:
    start = EmptyOperator(task_id="start")

    # A task that will succeed
    success_task = PythonOperator(
        task_id="success_task",
        python_callable=lambda: print("This task succeeds."),
        on_success_callback=send_success_email,  # Example of success callback
    )

    # A task that will fail and trigger the on_failure_callback
    fail_task = PythonOperator(
        task_id="fail_task",
        python_callable=failing_task,
    )

    end = EmptyOperator(task_id="end")

    # Set up dependencies
    start >> [success_task, fail_task] >> end