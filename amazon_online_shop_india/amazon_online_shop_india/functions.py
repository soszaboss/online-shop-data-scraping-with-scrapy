import amazon_online_shop_india.settings as settings

def list_product_details_into_dict(product_details: list):
    cleaned_details = [detail.strip() for detail in product_details if detail.strip()]
    if len(cleaned_details) % 2 != 0:
        cleaned_details.remove(cleaned_details[-1])
    cleaned_details = [detail for detail in cleaned_details if detail != '\\n']
    return [{cleaned_details[i]: cleaned_details[i + 1] for i in range(0, len(cleaned_details), 2)}]

def get_proxy_url(url: str):
    return f'https://proxy.scrapeops.io/v1/?api_key={settings.SCRAPEOPS_API_KEY}&url={url}'
