from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.hooks.base import BaseHook
from airflow.models import Variable
from datetime import datetime, timedelta
import requests
import psycopg2
from psycopg2 import sql


default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

TABLE_NAME = 'shopee_ratings'

dag = DAG(
    dag_id='crawl_shopee_ratings_split_tasks',
    default_args=default_args,
    start_date=datetime(2025, 8, 1),
    schedule='@daily',
    catchup=False,
    description='DAG crawl Shopee ratings and save to PostgreSQL (split tasks)',
    tags=['shopee', 'ratings']
)

# ------------------- TASK 1: Fetch Shopee ratings -------------------
def fetch_data_from_shopee(**context):
    url = "https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&limit=2&offset=0&type=0&exclude_filter=1&filter_size=0&fold_filter=0&relevant_reviews=false&request_source=2&tag_filter=&variation_filters=&fe_toggle=%5B2%2C3%5D&shopid=487028617&itemid=29911154536&preferred_item_item_id=29911154536&preferred_item_shop_id=487028617&preferred_item_include_type=1" #
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "af-ac-enc-dat": "3e8753c81dc9a5bd", #
        "af-ac-enc-sz-token": "DM+ifFf8HpYhl5lHTLmh9A==|iPHWMQ8SnuPbEYf/qy/emnWuDPcDbwpY/QJdQx1xMzQhEv6hnfKBHsCgp7+YL8H0ccqfAaBDt4hjZnFj|E9S6bKuiBbShck7F|08|3", #
        "content-type": "application/json",
        "referer": "https://shopee.vn/shop/487028617/item/29911154536/rating",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',  
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
        "x-api-source": "rweb",
        "x-csrftoken": "oO4ZvdS1lhSae6iCm6hXnvyFJHm9Rfy8",
        "x-requested-with": "XMLHttpRequest",
        "x-sap-ri": "116595688e22ddfbc2f3fb380701cc8c137565f2ca4c2205298a", #
        "x-sap-sec": "O19b86mfTfztq4l+IIp6lNlvBSGmjWT95bEMooLrXIvV0ecQaVS3K0qC0Qo13/N5yOQZwoXxZslvUP743QlGmZtKQAFcCcRP9Z9l8O41S939PenE0D584YTfLmAt/0Ksod2FuASZiir1gvf/YkfjykJa9UCcMgQsdZsDPXZhdJ5AGZ2BRxFWo6xgSlDKBKBcRMDejhVrPtz1m8VOXGmhkwPO37yD6QmYDurAcX1AssXluFH6vNHtJbhGMacz0mlHb0K1Jdoabp0DLMQMJc7GcVvY0p15HJ0jdIRBN8ao5Auy8y4IuyGWzVj6GaX8hlRVh2yJU8zXbcJmL3gLPIISyEWQtYTT18XkH9XSwsEg6P9E5T0h/ndxmTLV4oNKMTqWExgF9jTkk00lqOlXVUM4n9+kjSCRBJ3alVKxIGr9VYnrVXcnHWj/GPJNs6iToaXJ/4CMvika2ltiz72yfXeehfgw2k75LubJnwd3u1RLASLyeJ/DfftjM44OzRzTZms5YVSEdeqjxvjGgOh5IGQeRpM9MSB+QG77Sl+VuATS+dAH8jU+LOtBw9WC3RSiGhtwZFRZ+/GDmXmVN5Q+kGd9EqnUlvYWgZm9ac5v/tK9vriEEiioilUEGxcX9veq4DRGm2RWgYmsvTUDMf9Tg1udu9tc0X+ieK6pRXdctDlapxLYY46LsZXzQtrKFk/xD/B4SGufQYEqZXDHLtPRfPMusodT5nVCfpwE5nwrfiH3EEYvXN7JyKBM05uNeT6oZ5eGQnPcHxksaicqOJ7pwob11gAivLaJwrGOGSRZpzt8fzBfxKIaAWG7iOxqp5jGJTEKbYrgyOalmG8Gj1QvxHYfbA82+C7MjMuCOwaZGEYZTaO7C3r2139sLfKRbQJWJla966Df2dsgDW/HfyFxmmExW/1EHk6rU5lSvt/tzgKCQR+/FcmB4FwOSVYEEUUR+8yFTXZrSj/MbnsdggX6vTYyrOPBi7yt1FKMK+894mXbjy2rh8cr5kA6sV51x/ouIy2CPLiqTmryprfQzqJTyCursoq5lcqQ5dQr/N9tbfiH1Mt4Sji5m+6NGPUZ3i8ImFr1rhUudi88woI4v64sB/cSPXyZkOrBY2SKV1nB9UHQnDz8p57X/sia2sRFq3oXIoP5XAamh31q+VTg3SAVavjlej1kC6xyHX6nC79T+n9OXwxkC4t0eb9YrLIA7UFXm317JuHcffjxXwFzVK6kRvJqRQcC3eYV79/I+RyXN0oNrahCA9bFFgfZxJ4mxiUk3G1usM9qwRgBgKYIVsBfKT5fUNLM/fxmzpcqVyNYgrUF0fDxzGf8xmsrpZZsesLfXQRn+0WYxWg59CtSPMJ2UInGRlIH1tyjBShlFjKosfDhrZSVP8Ig07cHXWgMDqz1IQL7METS/bsJhxAgqkmUkqykv6igpHe01waRLA9tve0QUWamXfnyQ68BEo76/0HaeKwJl4tsznSpKl1FEFlcJ//bAxFyt3XafJtUzte442l44bk4f3UjW7HrPnfFxBiztheW66KKeqAtyZsnvY946XgNqo3v2ieS5LabvoRZ8NL3uJuQ67DUxljqOjxPynhma4BrH6RhlHBmMjtTyHaNwVXzm1azWwoyJ9GqY23LT6KqwdFODmHMPluG0bNOXpCj5C4v6AAhtWd25lPiZbKL9fxe1TwHGYSnVRZxb49gbznGQDSsKuOJXO4U1I0As1fM1IxbkFopb7vM0FhKTTIuJM/VYvy+cbOt/NOQCmQzF9cnWdSRTzXDUj1tKqILg14iRvCdYzCnZZY1RQY/hhpOk1wixlxVb+Hgmvh6bFVbItUhdQiulTMdw0C334PYYDwcDkxwMw7vaQIQUhWdo/JKdSwx7ZGADrTvfWDdpq3nDYQ0Ln8G0Kd/TWv3/3qNuzWGD8iCSfemzNf0HWFU04NbwtcrV1umKsBx8Nle1BALqcSpqYFErAM9GeHXdyuJKP3HuHKUtGeQED3ZZ+kAdJIJrXZnV3Ii5PXavSGcOjI4/dvdtHpF6e4XhaipWqHt85aG/IWmpKuiu9sd/GBeTsZcLduvHI0vdRf5NTFazV8vTS9yK+sRYgIcT4AD5MlUdbaD9Hpa9qE0SOfvmWbi3BmxRQnwVhGiOMYDwEuntSV2KrdIY4jEl+1ICPrmqTNQusO5IIeDAciMzzDxTsW29Oj9FRY0U3/YQEeG3OrSSK==", #
        "x-shopee-language": "vi",
        "x-sz-sdk-version": "1.12.21"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error fetching data: {response.status_code}")
    
    data = response.json()
    ratings = data.get("data", {}).get("ratings", [])

    if not ratings:
        print("No ratings found.")
        return []

    # Push to XCom for next task
    context['ti'].xcom_push(key='ratings_data', value=ratings)

fetch_task = PythonOperator(
    task_id='fetch_data_from_shopee',
    python_callable=fetch_data_from_shopee,
    dag=dag
)

# ------------------- TASK 2: Create table if not exists -------------------
def prepare_postgres_table():
    airflow_conn = BaseHook.get_connection("local_postgres")

    with psycopg2.connect(
        host=airflow_conn.host,
        port=airflow_conn.port,
        dbname=airflow_conn.schema,
        user=airflow_conn.login,
        password=airflow_conn.password
    ) as conn:
        with conn.cursor() as cur:
            create_table_query = sql.SQL("""
                CREATE TABLE IF NOT EXISTS {} (
                    id SERIAL PRIMARY KEY,
                    orderid BIGINT,
                    itemid BIGINT,
                    cmtid BIGINT,
                    ctime TIMESTAMP,
                    rating INTEGER,
                    rating_star INTEGER,
                    userid BIGINT,
                    shopid BIGINT,
                    comment TEXT,
                    status INTEGER,
                    mtime TIMESTAMP
                )
            """).format(sql.Identifier(TABLE_NAME))
            cur.execute(create_table_query)
        conn.commit()

prepare_table_task = PythonOperator(
    task_id='prepare_postgres_table',
    python_callable=prepare_postgres_table,
    dag=dag
)

# ------------------- TASK 3: Save to PostgreSQL -------------------
def save_ratings_to_postgres(**context):
    ratings = context['ti'].xcom_pull(key='ratings_data', task_ids='fetch_data_from_shopee')
    if not ratings:
        print("No data to insert.")
        return

    airflow_conn = BaseHook.get_connection("local_postgres")
    with psycopg2.connect(
        host=airflow_conn.host,
        port=airflow_conn.port,
        dbname=airflow_conn.schema,
        user=airflow_conn.login,
        password=airflow_conn.password
    ) as conn:
        with conn.cursor() as cur:
            insert_query = sql.SQL("""
                INSERT INTO {} (
                    orderid, itemid, cmtid, ctime, rating,
                    rating_star, userid, shopid, comment,
                    status, mtime
                )
                VALUES (%s, %s, %s, to_timestamp(%s), %s,
                        %s, %s, %s, %s, %s, to_timestamp(%s))
            """).format(sql.Identifier(TABLE_NAME))

            for r in ratings:
                cur.execute(insert_query, (
                    r.get("orderid", 0),
                    r.get("itemid", None),
                    r.get("cmtid", None),
                    r.get("ctime", None),
                    r.get("rating", None),
                    r.get("rating_star", None),
                    r.get("userid", None),
                    r.get("shopid", None),
                    r.get("comment", ""),
                    r.get("status", None),
                    r.get("mtime", None)
                ))
        conn.commit()

save_data_task = PythonOperator(
    task_id='save_ratings_to_postgres',
    python_callable=save_ratings_to_postgres,
    dag=dag
)

# ------------------- TASK 4: Log done -------------------
def log_success():
    print("Ratings saved successfully to PostgreSQL!")

log_task = PythonOperator(
    task_id='log_success',
    python_callable=log_success,
    dag=dag
)

# ------------------- DAG Flow -------------------
fetch_task >> prepare_table_task >> save_data_task >> log_task
