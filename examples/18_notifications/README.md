# 18 - Notifications and Alerts

Set up notifications and alerts for task success and failure using callbacks and operators.

## Overview
This DAG demonstrates:
- Using `on_failure_callback` to execute a function when a task fails
- Using `on_success_callback` to execute a function when a task succeeds
- Example of sending an email on success (requires email configuration in Airflow)
- How to set up a DAG-level failure callback

## How it works
1. **success_task**: A PythonOperator that prints a message and has an `on_success_callback` that attempts to send an email.
2. **fail_task**: A PythonOperator that is designed to fail (raises a ValueError) and triggers the `on_failure_callback`.
3. The DAG also has an `on_failure_callback` set at the DAG level, which will be called for any task that fails in the DAG.

## Prerequisites for email notifications
To actually send emails, you need to configure email settings in your `airflow.cfg` or set environment variables:
- `smtp_host`
- `smtp_starttls`
- `smtp_ssl`
- `smtp_user`
- `smtp_password`
- `smtp_mail_from`

Alternatively, you can use the `EmailOperator` for a more integrated approach (not shown in this example for simplicity).

## Run
```bash
airflow dags trigger notifications_dag
```

## View Results
- Check the logs for the `fail_task` to see the `on_failure_callback` output.
- Check the logs for the `success_task` to see if the email was sent (if email is configured).
- If email is not configured, the `send_email` function will raise an exception, which will be visible in the logs.