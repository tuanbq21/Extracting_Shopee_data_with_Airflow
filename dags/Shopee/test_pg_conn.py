from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime

with DAG(
    dag_id='local_postgres_dag',
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    create_table = SQLExecuteQueryOperator(
        task_id='create_table',
        conn_id='local_postgres',
        sql="""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            );
        """,
    )

    insert_data = SQLExecuteQueryOperator(
        task_id='insert_data',
        conn_id='local_postgres',
        sql="INSERT INTO users (name) VALUES ('Hải đẹp trai');",
    )

    create_table >> insert_data
