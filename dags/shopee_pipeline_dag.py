from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import requests
import json
import csv
import os
import psycopg2

# Đường dẫn thư mục
RAW_DIR = "/opt/airflow/data/raw"
PROCESSED_DIR = "/opt/airflow/data/processed"

# Crawl Task
def crawl_data():
    url = "https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&limit=2&offset=0&type=0&exclude_filter=1&filter_size=0&fold_filter=0&relevant_reviews=false&request_source=2&tag_filter=&variation_filters=&fe_toggle=%5B2%2C3%5D&shopid=487028617&itemid=29911154536&preferred_item_item_id=29911154536&preferred_item_shop_id=487028617&preferred_item_include_type=1"
    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "af-ac-enc-dat": "7bcab5b2a6e0443d", #
        "af-ac-enc-sz-token": "kjhjw6eDHmhfC91Z3zBj1w==|vPHWMQ8SnuPbEYf/qy/emnWuDPcDbwpY/QJdQ5Nt6CshEv6hnfKBHsCgp7+YL8H0ccqfAaBDt4hjZnFj|E9S6bKuiBbShck7F|08|3", #
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
        "x-sap-ri": "74ac99686de9a58fb3cec4380701aac3031dcab9f97cc1dbc1ad", #
        "x-sap-sec": "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", #
        "x-shopee-language": "vi",
        "x-sz-sdk-version": "1.12.21"
    }


    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        os.makedirs(RAW_DIR, exist_ok=True)
        file_path = os.path.join(RAW_DIR, f"shopee_ratings_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(response.json(), f, ensure_ascii=False, indent=2)
        print(f"Saved raw JSON to {file_path}")
    else:
        raise Exception(f"Error fetching data: {response.status_code}")

# Transform Task
def transform_data():
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # lấy file JSON mới nhất trong thư mục raw
    files = sorted([f for f in os.listdir(RAW_DIR) if f.endswith(".json")])
    if not files:
        raise Exception("No raw files found")
    latest_file = os.path.join(RAW_DIR, files[-1])

    with open(latest_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    ratings = data.get("data", {}).get("ratings", [])
    csv_path = os.path.join(PROCESSED_DIR, f"ratings_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
    with open(csv_path, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["comment", "rating_star"])
        for r in ratings:
            writer.writerow([r.get("comment", ""), r.get("rating_star", "")])

    print(f"Saved processed CSV to {csv_path}")

# Load Task (ví dụ insert vào DB giả lập)
def load_data():
    # Lấy file CSV mới nhất trong thư mục processed
    files = sorted([f for f in os.listdir(PROCESSED_DIR) if f.endswith(".csv")])
    if not files:
        raise Exception("No processed files found")
    latest_file = os.path.join(PROCESSED_DIR, files[-1])

    # Kết nối DB
    conn = psycopg2.connect(
        host="postgres",  # hoặc localhost
        port=5432,
        database="mydb",
        user="postgre",
        password="123456"
    )
    cursor = conn.cursor()

    # Đảm bảo bảng tồn tại
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shopee_ratings (
            id SERIAL PRIMARY KEY,
            comment TEXT,
            rating_star INT
        )
    """)
    conn.commit()

    # Đọc dữ liệu CSV và insert
    with open(latest_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO shopee_ratings (comment, rating_star)
                VALUES (%s, %s)
            """, (row["comment"], int(row["rating_star"]) if row["rating_star"] else None))

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Inserted data from {latest_file} into PostgreSQL successfully!")

# DAG
with DAG(
    dag_id="shopee_ratings_pipeline",
    start_date=datetime(2025, 8, 11),
    schedule="@daily",
    catchup=False,
    tags=["crawl", "transform", "load"]
) as dag:

    crawl_task = PythonOperator(
        task_id="crawl",
        python_callable=crawl_data
    )

    transform_task = PythonOperator(
        task_id="transform",
        python_callable=transform_data
    )

    load_task = PythonOperator(
        task_id="load",
        python_callable=load_data
    )

    crawl_task >> transform_task >> load_task
