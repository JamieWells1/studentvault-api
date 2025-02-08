import requests
from config.const import PROXY, DEV_URL

result = requests.get(DEV_URL, proxies={"http": PROXY["url"], "https": PROXY["url"]})
print(result.text)
