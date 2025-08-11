import requests
import json

# url = "https://shopee.vn/api/v2/item/get_ratings"

# params = {
#     "flag": "1",
#     "limit": "10",
#     "request_source": "3",
#     "exclude_filter": "1",
#     "fold_filter": "0",
#     "relevant_reviews": "false",
#     "itemid": "29911154536",
#     "shopid": "487028617",
#     "filter": "0",
#     "inherit_only_view": "false",
#     "fe_toggle": "[2,3]",
#     "preferred_item_item_id": "29911154536",
#     "preferred_item_shop_id": "487028617",
#     "preferred_item_include_type": "1",
#     "offset": "0"
# }


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
    "x-sap-sec": "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", #
    "x-shopee-language": "vi",
    "x-sz-sdk-version": "1.12.21"
}


response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json())