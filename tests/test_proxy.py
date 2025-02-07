import requests
from config.env_vars import PROXY

result = requests.get(url, proxies={"http": PROXY["url"], "https": PROXY["url"]})
print(result.text)
