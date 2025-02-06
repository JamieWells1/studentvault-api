import requests

url = "https://ip.smartproxy.com/json"
username = "spcjl3kcj6"
password = "pexigQ24E0x0=dMYcu"
proxy = f"http://{username}:{password}@gate.smartproxy.com:10005"
result = requests.get(url, proxies={"http": proxy, "https": proxy})
print(result.text)
