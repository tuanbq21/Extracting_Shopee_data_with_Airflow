import requests
import json

# url = "https://shopee.vn/api/v4/shop/search_items?filter_sold_out=1&item_card_use_scene=search_items_popular&limit=30&offset=0&order=desc&shopid=895406956&sort_by=pop&use_case=4"

# headers = {
#     "accept": "application/json",
#     "accept-encoding": "gzip, deflate, br, zstd",
#     "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
#     "af-ac-enc-dat": "7aa14ba961f36df2",
#     "af-ac-enc-sz-token": "Aj/npbw1TJsTOOmnKnmyJA==|2fHWMQ8SnuPbEYf/qy/emnWuDPcDbwpY/QJdQxoauwEhEv6hnfKBHsCgp7+YL8H0ccqfAaBDt4hjZA==|E9S6bKuiBbShck7F|08|3",
#     "priority": "u=1, i",
#     "referer": "https://shopee.vn/hmkeyewear",
#     "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": '"Windows"',
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
#     "x-api-source": "pc",
#     "x-csrftoken": "oO4ZvdS1lhSae6iCm6hXnvyFJHm9Rfy8",
#     "x-requested-with": "XMLHttpRequest",
#     "x-sap-ri": "7148a068108ccac6d067263807011a7cb96be6bf42a047d1f62f",
#     "x-sap-sec": "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",
#     "x-shopbff-version": "2025072400",
#     "x-shopee-language": "vi",
#     "x-sz-sdk-version": "1.12.21"
# }

import requests

url = "https://tiki.vn/api/personalish/v1/blocks/listings?limit=10&sort=top_seller&page=1&urlKey=xe-may&category=8597"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "accept": "application/json",
    "referer": "https://tiki.vn/"
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json())  # thử in raw text trước
