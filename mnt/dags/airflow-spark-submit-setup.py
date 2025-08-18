from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime
from airflow.operators.empty import EmptyOperator as DummyOperator
from airflow.operators.python import PythonOperator
from airflow.sdk import Variable

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 0,
}

def foo_func(**kwargs):
    logical_date = kwargs["logical_date"]
    print(f"Execution date: {logical_date}")
    print(f"All kwargs: {kwargs}")
    # return kwargs

with DAG(
    dag_id='spark_submit_example',
    default_args=default_args,
    # schedule='@hourly',
    schedule=None,
    catchup=False
) as dag:
    start_task = DummyOperator(task_id='start')
    
    python_operator_test = PythonOperator(
        task_id="python_operator_task",
        python_callable=foo_func,
        # provide_context=True Not required in Airflow 3.0
    )
    

    spark_submit_task = SparkSubmitOperator(
        task_id='spark_submit_test',
        application='hdfs://namenode:8020/user/spark/scripts/spark_udtf_exmple.py',
        conn_id='spark_default',
        conf={
            "spark.yarn.appMasterEnv.PYSPARK_PYTHON": "python3",
            "spark.executorEnv.PYSPARK_PYTHON": "python3",
            "spark.yarn.dist.files": "hdfs://namenode:8020/user/spark/jars/pyspark.zip,hdfs://namenode:8020/user/spark/jars/py4j-0.10.9.9-src.zip"
        },
        application_args=[],
        executor_cores=1,
        executor_memory='1G',
        num_executors=2,
        name='spark_udf_test',
        verbose=True,
        deploy_mode='cluster'
        # master='spark://spark-master:7077'    
    )
    end = DummyOperator(task_id='end')
    start_task >> python_operator_test >> spark_submit_task >> end