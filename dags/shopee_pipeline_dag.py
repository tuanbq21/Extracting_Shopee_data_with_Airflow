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
        "authority": "shopee.vn",
        "method": "GET",
        "path": "/api/v2/item/get_ratings?filter=0&flag=1&limit=2&offset=0&type=0&exclude_filter=1&filter_size=0&fold_filter=0&relevant_reviews=false&request_source=2&tag_filter=&variation_filters=&fe_toggle=%5B2%2C3%5D&shopid=487028617&itemid=29911154536&preferred_item_item_id=29911154536&preferred_item_shop_id=487028617&preferred_item_include_type=1",
        "scheme": "https",
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "af-ac-enc-dat": "b9fe1ae10eb1bc00",
        "af-ac-enc-sz-token": "2InOmY5pWjYVvWCPSi6+nw==|uPHWMQ8SnuPbEYf/qy/emnWuDPcDbwpY/QJdQ9YjMSshEv6hnfKBHsCgp7+YL8H0ccqfAaBDt4hjZnFj|E9S6bKuiBbShck7F|08|3",
        "content-type": "application/json",
        "cookie": "_QPWSDCXHZQA=7c814c42-2a5a-411a-89bc-d10bb2eee6a0; REC7iLP4Q=f6d4eedb-5a4d-4959-a73c-c46279c961dc; SPC_F=ZYxGZMi246jCkaboTG6T7Ly13NtQgqSg; REC_T_ID=c64889aa-50de-11f0-8d48-123f085b8545; SPC_CLIENTID=ZYxGZMi246jCkabombtsekhtpzsiebxi; csrftoken=oO4ZvdS1lhSae6iCm6hXnvyFJHm9Rfy8; _sapid=7e338a90c442d0f87b6e4692f2bf0e7379d1cf8ff43746f2fe49f51c; SPC_SC_SA_TK=; SPC_SC_SA_UD=; SPC_SC_OFFLINE_TOKEN=; SC_SSO=-; SC_SSO_U=-; SPC_SC_SESSION=; SPC_ST=.SnpUQnF2b0xwWlNRV21od5BdZ7J2QCfeN6lDWfVkHiGUxdynr+zdVuyUbatvxVC6AQZGv+p3R+9/wL98d8Gtu4vARcMGi76vHa0wW+cgmOfoSmvtmtC69TF17RCsRstgULBsxW3y8WIrHELeSGsv0pAx5GMXrZXwGU7tD+zqsh6gtAzbhHGMUMQqFscyXyVgzdCfTaTQin9LaKLCLtP9V5Yw8ZcMUmFoHVhGZwA/gnEtOiL78nCc0KZDTgIgmlQe; SPC_U=1167420699; SPC_R_T_ID=/G8sm/hB6uaZQ7Fcb7grUUPiEsn+OhyaTtUJNBN1ign0JrbWm4WWhUEXP6jAOnfP9xsMB+JxyjHPPWZZTRiiEE0kWIALogQHLFFI8uIdTWnFdEffItYF154DuC/+nGGKKWyn+D0vrR71a92IxuheHMq0dRHgiC/6t2zSqsmjym4=; SPC_R_T_IV=enh6ODJwUkxtUnhvZEFzZA==; SPC_T_ID=/G8sm/hB6uaZQ7Fcb7grUUPiEsn+OhyaTtUJNBN1ign0JrbWm4WWhUEXP6jAOnfP9xsMB+JxyjHPPWZZTRiiEE0kWIALogQHLFFI8uIdTWnFdEffItYF154DuC/+nGGKKWyn+D0vrR71a92IxuheHMq0dRHgiC/6t2zSqsmjym4=; SPC_T_IV=enh6ODJwUkxtUnhvZEFzZA==; SPC_CDS_CHAT=0816a2e7-04e4-431b-86ae-041b3e0b1131; SPC_IA=1; SPC_SI=aUB3aAAAAABEUEZDUGpQbTo18wEAAAAAYXZXRTJYcnE=; SPC_SEC_SI=v1-aFE5S1B3bGN2Ung1ZzJYWMKt7qLulxa9HRVFUAYzIu4MJ/pcnkXR4SLHj6Ycb5/s68ITJhAH26v6FSqhU5F/pmeeZ0K08ZKZ2OesJYuFFkk=; shopee_webUnique_ccd=2InOmY5pWjYVvWCPSi6%2Bnw%3D%3D%7CuPHWMQ8SnuPbEYf%2Fqy%2FemnWuDPcDbwpY%2FQJdQ9YjMSshEv6hnfKBHsCgp7%2BYL8H0ccqfAaBDt4hjZnFj%7CE9S6bKuiBbShck7F%7C08%7C3; ds=9656ebd69c92afd7506917eb901c16f7; SPC_EC=.Y2pERFVRS1RkV096Mk9jbkcSc+4Iem5VvTZHuFpAY5J1bDri+4I4OpKZuLuV4T/raQljQ3rrAPWzMJE76SUypj3rMJzFcsjjzk63NBfTHg9nRfFLCkL4yMFUb8meHO7nwNe1QhMJ6BQjXWZY1zuGemay/3LCt7OHgY/8mGKGuHE5durKA1gth4KJW9hmsC8DcmvOlBBxxt4ZPhBKb0A2XtRpBtsz7lg6yJP0miA0rvGC+yovasb4jsIY3zd98DB9",
        "priority": "u=1, i",
        "referer": "https://shopee.vn/product/487028617/29911154536",
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
        "x-sap-ri": "b6be9968e86761152d0d243f07016bebe4b313294570afac0eab",
        "x-sap-sec": "biZH86l2bdvQj+2Wi4uWikjWU4q2iPwW14qEiOpWuyqIiOAWF4qCirwWT4qvikrWX4qXiJ2Wx4uRiJjWbduBiI2WC4uIiIuWm4uCi5wWy4uVi4pWjyqTi4uWi4uW+MwWi4uWi4qqv4uWiOJ/0TAQiduWLBTdrmp8i4tLN1Seu4VWiPDARnQWiduWi5jQPVBeWVKWiduWi4uWcow8i4uWi4Lir4VWiow8i4uIiTuWF4XWisu9i4uWi4uN+lwWp229i4tCiyuWH4AWiIwFi4uWi4tgf4uWikE6/4i7pgrik4uWiE5AWDnzFU4az/T4aW2hD5wVDtGD9kH/t1wp5Y593X8v0e78wn+8zoI3L42sC4UKGLiAbkzXt+NiPOa6WUcFvNign8fCHhf+TyFNbKLVTON8TETNY4AEPYe2FMkYNGvKUGzrVWYnc6ihw5elQYI6CHedhF6dHbW6Zoek/d63VsgXYufxdm9OXeP4SOAxF4qM1zzLbtTJLsyMuCZvqL0U6qEqVWdnEu9btANA+0EEduXEdGwKKyKHoyz6qmgVS0QW7TpWi4qWWFYL7h6gnDRWi4uPBY0dg27mZcPz5gjw+XYIwwnnV5UXggV34S27W2ynC8Q1MlSvJ9ArvoMUa9Il84qZi4uWzPacYB6tM0vihbLxqbx67TNHtBAviuwoTxChr2qh1V+kplw8WuzTcBFKXdGjdH6RSYBKUSkgCStzSUQHkyCMiqrspIdHXoqJufrLiq2L32DGLTbz/qw3LbC7NoEwi4uWf4uWiJHNqFHRbfjRjduWi5My5Favi4uWiTuWi5cMi4uWi4uWq4uWikQQRStK89paPlrYf2FGMVZ0wyOYkBn7fdm4KDdO9sM9w/c0nOPsnr6zIAzIzUicXzcWmrBeAPcrX5E+GmNDeyLHBVdkrjg/zz2PVMRBiQ5Xj7toQiO0WWgWq6ByprjpympWi4q7Q15cX1iXYDOuMJwY5z2oUV31qiOg9luHP2kO819UYMBTJJzZ++9QGYJua+OgmIuHQ126lp9u17wWi4qsLdSqZ25OcMWGym1aUdx77yOCAkbGPj/1lX7imaaR2lUhi8rkGUK8ig9qgDhoPVifSCWAXQiK/fVUcMhlZhTH9vwIcUy7EaXlY0MDwEx4O1BRSaXGpuwKvRV0Nq4XQnO0hbAAzCI+KSGtN3VytjATKsgQ/yUa0UCPUt5Y18oisr880bR9i4uWyvXWie2Wi4uwjSmdCXr61wlAuNiDBuCNNZ41JFr8Wso+fBj/yGEfDEUvTI7iqz+pKQFoyuwJr13gWdybFaDfcKl3bVa7DMOvjh+aTgfzMpVuAi2kcle8WrtsnIy6DewCEczyvw7ZSVX+N2bl7jmAgEhAiPxu3Tz9NWg3HdYjWwY4Q8ZSSIK2OrANAMHpXcbbE6h804+vNsoD6YGCiQb3WvXSENrQVmgvdXPGLILD21dpimUQI+JC4GUPgXxgvgZlrpSUWXrWi4t5IK0xAyeoFJNpZIG07wEWqBxt6cILLo9XSRn+13haelAnDqT2UvcxSSKnLL616bOZwBSOWhhJgil4NxicsayVoCyj+2vXGMG6v6HNqbUCL2sWRICpMWqz9O2WiJu8i4nA5YFXgm/W81EisAArRbrjA1skQA1bPyB5DDsT9iFl+8/VNUeZP+VQOCt2lZll32EzjvePdn7VBfpFJ6zWpD7M89mOOJMZZWqBH9v9QYpfrxAnXPBNPMtBxGovTbMc9Rq1jBMoWL7Y41R0JfwhOetTFlY6GJN+H0x5kG+797cIt11AHpT35Pq8UUXrvJ5PdvBogPYJBj/hqRA1SL51jJGtjkodn3cgZFhj3l/HdzcEG6FGjLsipIJpzOBTvRij+DNgwzDirdU0/Q9JIbHbjef8XpPXp114h+99jV1jYhXS2KahSZy4NeejdzEsBgKSZDdAl2tG2kwkQ+kZHxmdWQzGVv/6wD6AQVQL6vmN0sVSmWzu3NcATpi5mh/s9LzhsYTg/r+dtnEBx4qFh2+FIBkEfduWi53TOOA2Rdo3xyuWis==",
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

def load_data():
    import psycopg2

    # Lấy file CSV mới nhất trong thư mục processed
    files = sorted([f for f in os.listdir(PROCESSED_DIR) if f.endswith(".csv")])
    if not files:
        raise Exception("No processed files found")
    latest_file = os.path.join(PROCESSED_DIR, files[-1])

    # Kết nối DB local
    conn = psycopg2.connect(
        host="host.docker.internal",  # để container Airflow truy cập PostgreSQL trên máy host
        port=5432,
        database="mydb",              # đổi đúng tên DB local
        user="postgres",              # user local
        password="123456"             # password local
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

    print(f"Inserted data from {latest_file} into local PostgreSQL successfully!")


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
