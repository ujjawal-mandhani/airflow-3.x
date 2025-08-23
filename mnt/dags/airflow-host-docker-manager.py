import subprocess
import json
import logging as log
from datetime import datetime, timedelta
from airflow import DAG
from airflow.models import Variable
from airflow.sdk import Variable
from airflow.operators.python import PythonOperator, BranchPythonOperator, get_current_context
from airflow.operators.empty import EmptyOperator as DummyOperator
from airflow.utils.task_group import TaskGroup
import json
from airflow.operators.bash import BashOperator
from airflow.models.param import Param


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 1, 1),
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

default_params = [
    "youtube-downloader-ui",
    "hive-example",
    "gitbook-docs",
    "qbittorrent",
    "filebrowser",
    "wireguard-vpn",
    "vault-warden"
]

def print_params_func():
    context = get_current_context()
    params = context["params"]
    if params["switch_turn_on_off"] == "on":
        docker_command = "docker-compose up -d"
    else:
        docker_command = "docker-compose down"
    script = f'''ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null root@host.docker.internal<<'EOF'
            cd /home/ujjawalmandhani/Desktop/Learning/{params["choose_docker_compose"]} 
            {docker_command}
        '''
    return script

def choose_branch_func():
    context = get_current_context()
    params = context["params"]
    print("::::::::::::::", params)
    return f"docker_compose_task_group.prepare_script_for_compose_up_or_down_{params["choose_docker_compose"]}"
    
with DAG(
    dag_id = 'airflow-host-docker-manager',
    default_args=default_args,
    description='airflow-host-docker-manager',
    catchup=False,
    schedule=None,
    params={
        "choose_docker_compose": Param(
            default=default_params[0],
            type="string",
            enum = default_params
        ),
        "switch_turn_on_off": Param(
            default='on',
            type="string",
            enum = [
                "on",
                "off"
            ]
        )
    }
):
    start_task = DummyOperator(task_id='start')
    
    choose_branch = BranchPythonOperator(
        task_id="branching",
        python_callable=choose_branch_func
    )
    
    with TaskGroup(group_id="docker_compose_task_group", tooltip="docker_compose") as docker_compose_task_group:
        for item in default_params:
            print_params = PythonOperator(
                task_id=f"prepare_script_for_compose_up_or_down_{item}",
                python_callable=print_params_func
            )
            task_bash_command = BashOperator(
                task_id=f"task_bash_command_for_compose_up_or_down_{item}",
                bash_command=(
                    f'{{{{ (ti.xcom_pull(task_ids="docker_compose_task_group.prepare_script_for_compose_up_or_down_{item}")) }}}}'
                )
            )
            print_params >> task_bash_command
            
    end_task = DummyOperator(task_id='end')
    start_task >> choose_branch >> docker_compose_task_group >> end_task
    