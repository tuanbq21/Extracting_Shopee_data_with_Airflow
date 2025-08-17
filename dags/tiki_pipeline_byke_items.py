from airflow import DAG     
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import requests, json, csv, os, psycopg2, sys
from repository.shopee_etl_repo import ShopeeETL
from dags.anonymous_path import Path_Folder

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))




url = "https://tiki.vn/api/personalish/v1/blocks/listings?limit=10&sort=top_seller&page=1&urlKey=xe-may&category=8597"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "accept": "application/json",
    "referer": "https://tiki.vn/"
}

conn = psycopg2.connect(
    host="host.docker.internal", 
    port=5432,
    database="mydb",              
    user="postgres",              
    password="123456"             
)

Path_Folder = Path_Folder()

hmkRepo = ShopeeETL(headers, url, conn)

json_key = "items"

# ===================================================================================
item_tags = [
    "id",
    "sku",
    "name",
    "brand_name",
    "short_description",
    "price",
    "list_price",
    "original_price",
    "discount",
    "discount_rate",
    "rating_average",
    "review_count",
    "order_count",
    "quantity_sold",
    "thumbnail_url",
    "thumbnail_width",
    "thumbnail_height",
    "badges_new",
    "seller_product_id",
    "url_key",
    "url_path",
    "shippable",
    "is_visible",
    "productset_id",
    "impression_info"
]


type_map = {
    "id": "BIGINT PRIMARY KEY",
    "sku": "VARCHAR(50)",
    "name": "TEXT",
    "brand_name": "TEXT",
    "short_description": "TEXT",
    "price": "BIGINT",
    "list_price": "BIGINT",
    "original_price": "BIGINT",
    "discount": "BIGINT",
    "discount_rate": "INT",
    "rating_average": "FLOAT",
    "review_count": "INT",
    "order_count": "INT",
    "quantity_sold": "INT",
    "thumbnail_url": "TEXT",
    "thumbnail_width": "INT",
    "thumbnail_height": "INT",
    "badges_new": "JSONB",
    "seller_product_id": "BIGINT",
    "url_key": "TEXT",
    "url_path": "TEXT",
    "shippable": "BOOLEAN",
    "is_visible": "BOOLEAN",
    "productset_id": "BIGINT",
    "impression_info": "JSONB"
}
item_tag = [tag for tag in item_tags if tag in type_map]
table_name = "tiki_byke_items"
cols = ",\n    ".join([f"{col} {type_map.get(col, 'TEXT')}" for col in item_tag])
command_load_0 = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id SERIAL PRIMARY KEY,
    {cols}
);
"""

command_load_1 = f"""
INSERT INTO {table_name} (
    {", ".join(item_tag)}
) VALUES %s
ON CONFLICT (id) DO UPDATE SET
    {", ".join([f"{col} = EXCLUDED.{col}" for col in item_tag if col != 'id'])}
"""

command_load = [command_load_0, command_load_1]

#===================================================================================
def crawl_data():
    hmkRepo.crawl(Path_Folder.raw_folder_path)

def transform_data():
    hmkRepo.transform(Path_Folder.processed_folder_path, Path_Folder.raw_folder_path, json_key, item_tag)

def load_data():
    hmkRepo.load_hmk_items(Path_Folder.processed_folder_path, command_load, item_tag)

with DAG(
    dag_id="tiki_pipeline_byke_items",
    schedule="@daily",
    start_date=datetime(2025, 8, 16),
    catchup=False,
    tags=["crawl", "transform", "load"]
) as dag:

    crawl_task = PythonOperator(
        task_id="crawl_hmk_items",
        python_callable=crawl_data
    )

    transform_task = PythonOperator(
        task_id="transform_hmk_items",
        python_callable=transform_data
    )

    load_task = PythonOperator(
        task_id="load_hmk_items",
        python_callable=load_data
    )

    crawl_task >> transform_task >> load_task
