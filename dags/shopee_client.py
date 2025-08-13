import requests

URL = "https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&limit=2&offset=0&type=0&exclude_filter=1&filter_size=0&fold_filter=0&relevant_reviews=false&request_source=2&tag_filter=&variation_filters=&fe_toggle=%5B2%2C3%5D&shopid=487028617&itemid=29911154536&preferred_item_item_id=29911154536&preferred_item_shop_id=487028617&preferred_item_include_type=1"

HEADERS = {
    "accept": "application/json",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/138.0.0.0 Mobile Safari/537.36",
    "x-api-source": "rweb"
    # ⚠️ Bỏ bớt header nhạy cảm và dài, chỉ giữ lại vài cái để ví dụ
}

def fetch_ratings(url=URL, headers=HEADERS):
    """
    Gọi API Shopee để lấy ratings.
    Trả về (status_code, json_data).
    """
    response = requests.get(url, headers=headers)
    return response.status_code, response.json()


if __name__ == "__main__":
    status, data = fetch_ratings()
    print("Status Code:", status)
    print("Response JSON:", data)
