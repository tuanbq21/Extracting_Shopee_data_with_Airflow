# Schedule_Crawl_Transform_Load

**Overview**  
`Schedule_Crawl_Transform_Load` is a Python-based project that implements a complete data pipeline workflow—**Crawl → Transform → Load**. With modular structure and Docker Compose support, it's designed for easy deployment and testing.

**Project Structure**  
- `dags/`: contains workflow definitions (e.g. for Airflow)  
- `config/`: configuration files (e.g. endpoints, credentials, schedule parameters)  
- `data/`: stores input/output data or intermediate results  
- `logs/`: execution logs for monitoring and debugging  
- `.env`: environment variables (e.g. DB credentials, API keys)  
- `docker-compose.yaml`: container orchestration for local setup  
- `shopee_ratings.csv`: sample dataset, likely from Shopee, for testing or demonstration

**Key Features**  
- Modular and clean architecture separating code, config, data, and logs.  
- Supports containerized deployment via Docker Compose.  
- Comes with sample data to showcase or test the full pipeline.

**Usage**  
1. Configure your variables in `.env`.  
2. Adjust settings in `config/` as needed.  
3. Launch the pipeline locally with `docker-compose up`.  
4. Monitor logs in `logs/` for pipeline execution status and debugging.

**Note**: You can expand this by adding documentation for any dependencies (e.g. Airflow setup), instructions to run specific DAGs, or sample outputs in the `data/` folder.

---

Nếu bạn muốn mình viết chi tiết thêm phần cách chạy (usage) hoặc hướng dẫn triển khai cụ thể (ví dụ: làm sao để chạy DAGs, tích hợp với Airflow, định dạng dữ liệu…), cứ nói nhé!
::contentReference[oaicite:1]{index=1}
