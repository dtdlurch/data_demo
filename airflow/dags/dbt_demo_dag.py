
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

def extract_placeholder():
    print("Extract step placeholder: in a real pipeline, fetch raw data or validate inputs.")

with DAG(
    dag_id="dbt_bigquery_demo",
    start_date=datetime(2024,1,1),
    schedule_interval=None,
    catchup=False,
    default_args={"owner": "airflow"}
):
    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_placeholder
    )

    dbt_build = BashOperator(
        task_id="dbt_build",
        bash_command="dbt deps && dbt build --profiles-dir /opt/airflow/dbt/profiles --project-dir /opt/airflow/dbt",
        env={"GOOGLE_APPLICATION_CREDENTIALS": "/opt/airflow/secrets/gcp.json"}
    )

    extract >> dbt_build
