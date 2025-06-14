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

 
def foo_func():
    print(json.loads(Variable.get("uat_project_id")))
    return json.loads(Variable.get("uat_project_id"))

 
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}
 
def my_function(xcom_value, **kwargs):
    print(":::::::::::::::", xcom_value.replace('\\\\\\\\', '/'))
    print(f"Pulled XCom value via template: {xcom_value}")

with DAG(
    dag_id = 'foo_example',
    default_args=default_args,
    description='foo_example',
    catchup=False,
    schedule=None,
) as dag:
 
    start_task = DummyOperator(task_id='start')

    dummy_task = PythonOperator(
        task_id="some_task",
        python_callable=foo_func,
    )
    
    pull_task = PythonOperator(
        task_id='pull_task',
        python_callable=my_function,
        op_args=["{{ ti.xcom_pull(task_ids='some_task') }}"],
        dag=dag,
    )
    end = DummyOperator(task_id='end')
 
    start_task >> dummy_task >> pull_task >> end
