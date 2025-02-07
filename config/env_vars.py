import os
import random

ports = [
    10001,
    10002,
    10003,
    10004,
    10005,
    10006,
    10007,
    10008,
    10009,
    10010,
    10011,
    10012,
    10013,
    10014,
    10015,
    10016,
    10017,
    10018,
    10019,
    10020,
    10021,
    10022,
    10023,
    10024,
    10025,
]

port = ports[random.randint(0, len(ports))]
print(port)

PROXY = {
    "username": "spcjl3kcj6",
    "password": "pexigQ24E0x0=dMYcu",
    "url": f"http://spcjl3kcj6:pexigQ24E0x0=dMYcu@gate.smartproxy.com:{10005}",
}

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
