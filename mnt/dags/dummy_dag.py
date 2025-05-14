import subprocess
import json
import logging as log
from datetime import datetime, timedelta
from airflow import DAG
# from airflow.models import Variable
from airflow.sdk import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator as DummyOperator


 
 
def foo_func():
    print(Variable.get("uat_project_id"))
    return Variable.get("uat_project_id")

 
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}
 
 
with DAG(
    dag_id = 'foo_example',
    default_args=default_args,
    description='foo_example',
    catchup=False,
    schedule=None,
) as dag:
 
    start_task = DummyOperator(task_id='start')

    dummy_task = PythonOperator(
        task_id=f"{Variable.get("uat_project_id")}",
        python_callable=foo_func,
    )
 
    end = DummyOperator(task_id='end')
 
    start_task >> dummy_task >> end
