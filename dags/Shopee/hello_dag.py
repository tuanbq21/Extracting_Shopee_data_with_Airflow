from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

def say_hello():
    print("Xin chào từ Airflow!")

with DAG(
    dag_id='hello_python_dag',
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:
    hello_task = PythonOperator(
        task_id='say_hello',
        python_callable=say_hello
    )
