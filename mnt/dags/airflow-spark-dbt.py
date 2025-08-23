import subprocess
import json
import logging as log
from datetime import datetime, timedelta
from airflow import DAG
# from airflow.models import Variable
from airflow.sdk import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator as DummyOperator
import json
# from airflow_dbt.operators.dbt_operator import DbtRunOperator
# from airflow_dbt_python.operators.dbt import DbtRunOperator
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}


with DAG(
    dag_id = 'airflow-spark-dbt',
    default_args=default_args,
    description='airflow-spark-dbt',
    catchup=False,
    schedule=None
):
    start_task = DummyOperator(task_id='start')
    
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=(
            "cd /opt/airflow/airflow-dbt-spark/airflow_dbt_spark && "
            "dbt run --select tag:hudi --profiles-dir /home/airflow/.dbt --target thrift-server"
        )
    )
    end = DummyOperator(task_id='end')
    start_task >> dbt_run >> end