import subprocess
import requests
import json
import sys
import os
import logging as log
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
# from airflow.providers.google.cloud.hooks.secret_manager import GoogleCloudSecretManagerHook
# from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator
# from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.empty import EmptyOperator as DummyOperator
from airflow.utils.task_group import TaskGroup


 
 
def query_executorBQ(query):
    print(query)
    # bq_hook = BigQueryHook(
    #     gcp_conn_id='google_cloud_uat',
    #     use_legacy_sql=False
    # )
    # result_df = bq_hook.get_pandas_df(query)
    # return result_df.to_dict(orient='records')
    return query
 
def check_smtp_availablity_func():
    try:
        output = subprocess.check_output(
            # ['curl', '-v', 'telnet://smtp.netcorecloud.net:587', '--max-time', '2'],
            ['curl', '-v', 'telnet://pl-1-ap-south-1.wohyz.mongodb.net:1025', '--max-time', '2'],
            stderr=subprocess.STDOUT,
            text=True
        )
        print("Command succeeded:\n", output)
    except subprocess.CalledProcessError as e:
        print("Command failed with exit code", e.returncode)
        print("Output:\n", e.output)
 
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}
 
 
with DAG(
    dag_id = 'chl_reconcilliation_report_dag',
    default_args=default_args,
    description='chl_reconcilliation_report_dag',
    catchup=False,
    # schedule_interval=None,
    schedule=None,
    tags=["reconcilliation", "reports"],
    # max_active_runs=1
) as dag:
 
    start_task = DummyOperator(task_id='start')
 
    with open('./dags/reconcilliation_config.json') as config_file:
        config_data = json.loads(config_file.read())
   
    with TaskGroup("dynamic_taskgroup") as task_group:
        for item in config_data:
            table_name = item["table_name"]
            table_schema = item["table_schema"]
            project_id = Variable.get("uat_project_id")
            query = f"SELECT COUNT(DISTINCT doc_id) AS mirror_cnts FROM `{project_id}.{table_schema}.{table_name}`"
            counts_from_bq = PythonOperator(
                task_id=f"{table_schema}_{table_name}",
                python_callable=query_executorBQ,
                op_args=[query]
            )
            counts_from_bq
 
    end = DummyOperator(task_id='end')
 
    start_task >> task_group >> end
