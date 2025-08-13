import requests

URL = "https://shopee.vn/api/v2/item/get_ratings?filter=0&flag=1&limit=2&offset=0&type=0&exclude_filter=1&filter_size=0&fold_filter=0&relevant_reviews=false&request_source=2&tag_filter=&variation_filters=&fe_toggle=%5B2%2C3%5D&shopid=487028617&itemid=29911154536&preferred_item_item_id=29911154536&preferred_item_shop_id=487028617&preferred_item_include_type=1"

HEADERS = {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
    "af-ac-enc-dat": "c2ca9b60dfb869f7",
    "af-ac-enc-sz-token": "V6HwPajAQNFYiLHSZNEDGw==|ovHWMQ8SnuPbEYf/qy/emnWuDPcDbwpY/QJdQwHP0REhEv6hnfKBHsCgp7+YL8H0ccqfAaBDt4hjZnFj|E9S6bKuiBbShck7F|08|3",
    "content-type": "application/json",
    "cookie": "_QPWSDCXHZQA=7c814c42-2a5a-411a-89bc-d10bb2eee6a0; REC7iLP4Q=f6d4eedb-5a4d-4959-a73c-c46279c961dc; SPC_F=ZYxGZMi246jCkaboTG6T7Ly13NtQgqSg; REC_T_ID=c64889aa-50de-11f0-8d48-123f085b8545; SPC_CLIENTID=ZYxGZMi246jCkabombtsekhtpzsiebxi; csrftoken=oO4ZvdS1lhSae6iCm6hXnvyFJHm9Rfy8; _sapid=7e338a90c442d0f87b6e4692f2bf0e7379d1cf8ff43746f2fe49f51c; SPC_SC_SA_TK=; SPC_SC_SA_UD=; SPC_SC_OFFLINE_TOKEN=; SC_SSO=-; SC_SSO_U=-; SPC_SC_SESSION=; SPC_ST=.SnpUQnF2b0xwWlNRV21od5BdZ7J2QCfeN6lDWfVkHiGUxdynr+zdVuyUbatvxVC6AQZGv+p3R+9/wL98d8Gtu4vARcMGi76vHa0wW+cgmOfoSmvtmtC69TF17RCsRstgULBsxW3y8WIrHELeSGsv0pAx5GMXrZXwGU7tD+zqsh6gtAzbhHGMUMQqFscyXyVgzdCfTaTQin9LaKLCLtP9V5Yw8ZcMUmFoHVhGZwA/gnEtOiL78nCc0KZDTgIgmlQe; SPC_U=1167420699; SPC_R_T_ID=/G8sm/hB6uaZQ7Fcb7grUUPiEsn+OhyaTtUJNBN1ign0JrbWm4WWhUEXP6jAOnfP9xsMB+JxyjHPPWZZTRiiEE0kWIALogQHLFFI8uIdTWnFdEffItYF154DuC/+nGGKKWyn+D0vrR71a92IxuheHMq0dRHgiC/6t2zSqsmjym4=; SPC_R_T_IV=enh6ODJwUkxtUnhvZEFzZA==; SPC_T_ID=/G8sm/hB6uaZQ7Fcb7grUUPiEsn+OhyaTtUJNBN1ign0JrbWm4WWhUEXP6jAOnfP9xsMB+JxyjHPPWZZTRiiEE0kWIALogQHLFFI8uIdTWnFdEffItYF154DuC/+nGGKKWyn+D0vrR71a92IxuheHMq0dRHgiC/6t2zSqsmjym4=; SPC_T_IV=enh6ODJwUkxtUnhvZEFzZA==; SPC_CDS_CHAT=0816a2e7-04e4-431b-86ae-041b3e0b1131; SPC_IA=1; SPC_SI=sxabaAAAAABmOGRBbTY0N/HpEQAAAAAAZW14dlNodGc=; SPC_SEC_SI=v1-OVlBYTFKVlE4Y0hEZlRtZXUKp9U9OaPKVJ3+KVNaVAg3DRmAuRcD2Uf8PWQBMIK9jD4/duTzus7ZPLHC0ri51lfuL1WcvLqHegD79S77gRA=; shopee_webUnique_ccd=V6HwPajAQNFYiLHSZNEDGw%3D%3D%7CovHWMQ8SnuPbEYf%2Fqy%2FemnWuDPcDbwpY%2FQJdQwHP0REhEv6hnfKBHsCgp7%2BYL8H0ccqfAaBDt4hjZnFj%7CE9S6bKuiBbShck7F%7C08%7C3; ds=1977e1d3c22eb18dbae7049758f26c75; SPC_EC=.dm1HeFVZSXozTEJBbGFETcyKxLiMA3ST7+skzmBwZpzh0aMro6+F8oXz50YcFQ5Ozeq2A8CINk0nASRMg/+YjHqWJNfM0YGyNWGJvED2kvLhum5GId46aQmpRtd7CVAxCRyizhuXVKKzE2ZFfZYJUyjUg6CfneGFobIA3t7cv5uL42H1px+TijGWaIseiXC2YNAZpCGQ85EGSfpRtMohntju5O2N2OPeaGEvvZGutJxqagKOh06FXLXbcAvktxG+",
    "priority": "u=1, i",
    "referer": "https://shopee.vn/product/487028617/29911154536",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "\"Android\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
    "x-api-source": "rweb",
    "x-csrftoken": "oO4ZvdS1lhSae6iCm6hXnvyFJHm9Rfy8",
    "x-requested-with": "XMLHttpRequest",
    "x-sap-ri": "ad459c68497183d95876283907014a6f5a1429d97c4f506a50b7",
    "x-sap-sec": "QNOSqK0aREuG2oeP0/UP00FPg/Vt0dZPivV80c3Px/Vc0cFPG/Vh0QZPY/vZ02PP5/vi003PO/vT00UPe/v00LZPS/ve0KPPs/v40KUPcvUG06ZPdvUj06UPM/Uq07ZP+/U303eP6xUM0/MPLxUh0/mPkxUP0/UPbS2F0/UP0/1dMNZP0/UP0NIDHFdGACnvgkFe0EUP+/tP0/UP02Zg0EUPzNCLV6DvYnim0EUP0/UPjbm23bMP0/1ON7cPJVlTZ8/5NCKoU/tP0/UP00730EUPc/FP0/UP0/nP0xUPs/FP0/UP0M0PIc540/UPoogV4mJrXZcw4EadJ2P1WgGRsNhl0/vgCrZr0/UP0vUPK/8P0con0MfdIM2hl/8P0L8P0/Vh/DSQSaNky3ZwUM6hINq4Fiu9+OijVaWjRFHx2wrtr56VGI5CtRrFZU3bGRHPxRE/Z3IIg7YuIM+U6vkCVx5eGHuC7SNra0l7O3oKlx1np1i1zEUF0/UPZ0JwN299gFusQHGXIr4bbFC1MuMuXXRSuqJm5p9TFOX+PVJF7vUP0NBAk7LVzRRrAqn9+1b8xB0oJhMP7vUP0+WAPSUTyi4qnYJUrqX6jMyOrSPPt/UP0Qab8GNPQSc2zeC88w+sfyhfUYPWY3sNWby1HA4ah0NkdvjHek5WiQJIDBK5WVJLc9+YBSXpplUK9gcTIXh9vM79Pjr+21tihWYKQ36DfIjzki0jxOXX4VDI41OfZmiD7TRgHVuCLn/oQWjNi3k8gGLhomvCfIPQO9Gws8OuPmuVdFFXl32vztCGq/CWSZf8b8n+jrQNrZxeUOtr81B60gg1x9+/+sjz1m50StVBzXnrIzmuoewjsFzamuVV3CwS4JZp0EqUDXWF8pETx/UP0/Ur0/UPFtZP0LcP0/vR5bfxOix0/7nlhf6ceEFX3K6WiVfnrfExsyKy6h7EHW4CjRBv+oxlTl72f6IBSOZeTTUiOSy8PJVGrD6CrZbW6plN6wYJ92K7IV/87hVCwBabAo0jrLosQ8+PQHzm0/Uh0/UPj/hrpnkdnyFh0/UPdoWFkoZzR69M0/UPvUOj7zw+FNnvbC++rWxLwIwYvk62UIcAThCDJvvgS1JjN0pMF2bX42MCTWjrbBlO3MJsftm6AViynAnw9vS9vDFI6g92C6GP6kXFAIVpogafDND6SPiwbnkdQiT1OiA6JcpJlrRNER3Y1Ycc4BQZt0Vv5vx/k+HtkQYLDJgxSvKHolRRVd46Ahu21qBzbuy63BjY4+J5yBCLgPTxQK1AxZq9JZSV7nlq7yVgwN3OoHaI5GYHLE0aqcjlSerjFEDPM7RQ/hwBSYGXj1j0SqhuNE3P0/VQQVnnIkyFxFtTRpgh0/UPY5R8n30YCD2G0/UPzyyifhCLTIQSNisLD2wRVkRVmSh8Xfn/nvnggAMMbmzxPVdcXuEU8KS7OC+pc9z/+ciPx7GC38tAH/jjw+hMVKtmp8pnknAz+NlzX35nCm0imKpjOc6l4+jVUXTVUCo+a1BorHnSEcHMLYZCU/VkS/EE9hD4mqq/HfXYT8FyhfNDAly5bz9zujUld3Fl/OgYnv0zjHVNEdUdIED92fId3QBS5Qj8O9m2OJ0VEsEfIf2ahSAYJU2U09PP0/UuGxPgOzVWq+He0kG3EVfg8vJxbIsHUpfTtP8zqUDvoNSEfTIgze+A3Q6KT6Htq/TOGZTJRg374g0ZecJZyU4T/w6UYr5gickigUVvoOlURUN/GpE3jGbY4vL5WxCRVkj5HeVyPpLs9VReIf8gwVL4Xux/BUxAThE6VxyCOGjEprsHSv7fwYFI1q+dv13/Yr8G3J4crnSmDn3WQg/ckTlrpvzz1bSoYdNPHSfAgoqJJxsdR8M9MewjyV4B+y8mwPTbnVMzZQU+ZDpCedA7In64GEg/7WBpZV2l8PTJMTV0QQoG5iy71s0o0U9l0K==",
    "x-shopee-language": "vi",
    "x-sz-sdk-version": "1.12.21"
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
