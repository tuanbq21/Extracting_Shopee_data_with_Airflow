from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator



# Định nghĩa args mặc định cho các task
default_args = {
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Tạo DAG
with DAG(
    'sprint_date_sleep_whoami',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule=timedelta(days=1),
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['example'],
) as dag:

    # Task 1: In ra “Starting the pipeline...”
    t1 = BashOperator(
        task_id='print_date',
        bash_command='date',
    )

    # Task 2: Ngủ 5 giây
    t2 = BashOperator(
        task_id='sleep',
        depends_on_past=False,
        bash_command='sleep 5',
    )

    # Task 3: In hostname
    t3 = BashOperator(
        task_id='print_whoami',
        bash_command='whoami',
    )

    # Định nghĩa thứ tự chạy
    t1 >> t2 >> t3
