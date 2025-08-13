import requests
import json


url = "https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&limit=2&offset=0&type=0&exclude_filter=1&filter_size=0&fold_filter=0&relevant_reviews=false&request_source=2&tag_filter=&variation_filters=&fe_toggle=%5B2%2C3%5D&shopid=487028617&itemid=29911154536&preferred_item_item_id=29911154536&preferred_item_shop_id=487028617&preferred_item_include_type=1"
headers = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
    "af-ac-enc-dat": "b9fe1ae10eb1bc00", #
    "af-ac-enc-sz-token": "2InOmY5pWjYVvWCPSi6+nw==|uPHWMQ8SnuPbEYf/qy/emnWuDPcDbwpY/QJdQ9YjMSshEv6hnfKBHsCgp7+YL8H0ccqfAaBDt4hjZnFj|E9S6bKuiBbShck7F|08|3", #
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
    "x-sap-ri": "b6be9968e86761152d0d243f07016bebe4b313294570afac0eab", #
    "x-sap-sec": "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 ", #
    "x-shopee-language": "vi",
    "x-sz-sdk-version": "1.12.21"
}



response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json())