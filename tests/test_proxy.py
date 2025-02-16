import requests
from config.const import PROXY, DEV_RESOURCE_URL

result = requests.get(
    DEV_RESOURCE_URL, proxies={"http": PROXY["url"], "https": PROXY["url"]}
)
print(result.text)
