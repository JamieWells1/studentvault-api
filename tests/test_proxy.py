import requests
from config.const import PROXY

result = requests.get(url, proxies={"http": PROXY["url"], "https": PROXY["url"]})
print(result.text)
