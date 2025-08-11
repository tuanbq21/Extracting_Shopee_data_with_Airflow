from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta
import json
import os
import psycopg2

RAW_DIR = "/opt/airflow/data/raw"
PROCESSED_DIR = "/opt/airflow/data/processed"

DB_CONFIG = {
    "host": "postgres",
    "port": 5432,
    "dbname": "mydb",
    "user": "postgre",
    "password": "123456"
}

def crawl_data(**kwargs):
    os.makedirs(RAW_DIR, exist_ok=True)
    data = {
        "time": str(datetime.now()),
        "items": [
            {"id": 1, "value": 100},
            {"id": 2, "value": 200}
        ]
    }
    file_name = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    file_path = os.path.join(RAW_DIR, file_name)
    with open(file_path, "w") as f:
        json.dump(data, f)
    kwargs['ti'].xcom_push(key='raw_file', value=file_path)
    print(f"Crawled data saved to: {file_path}")

def transform_data(**kwargs):
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    ti = kwargs['ti']
    raw_file = ti.xcom_pull(key='raw_file', task_ids='crawl')
    
    with open(raw_file, "r") as f:
        data = json.load(f)
    
    # Transform: nhân value lên 2 lần
    for item in data["items"]:
        item["value"] *= 2
    
    processed_file = os.path.join(PROCESSED_DIR, f"processed_{os.path.basename(raw_file)}")
    with open(processed_file, "w") as f:
        json.dump(data, f)
    
    ti.xcom_push(key='processed_file', value=processed_file)
    print(f"Processed data saved to: {processed_file}")

def load_data(**kwargs):
    ti = kwargs['ti']
    processed_file = ti.xcom_pull(key='processed_file', task_ids='transform')
    
    with open(processed_file, "r") as f:
        data = json.load(f)
    
    # Insert vào PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    for item in data["items"]:
        cur.execute(
            "INSERT INTO etl_results (id, value, created_at) VALUES (%s, %s, %s)",
            (item["id"], item["value"], datetime.now())
        )
    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded data from {processed_file} into DB.")

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "etl_pipeline_xcom_db",
    default_args=default_args,
    description="ETL pipeline: crawl -> transform -> load (Postgres)",
    schedule=timedelta(days=1),
    start_date=datetime(2025, 8, 10),
    catchup=False,
    tags=["crawl", "etl", "transform", "load", "postgres"],
) as dag:

    crawl_task = PythonOperator(
        task_id="crawl",
        python_callable=crawl_data,
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform_data,
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load_data,
    )

    crawl_task >> transform_task >> load_task
