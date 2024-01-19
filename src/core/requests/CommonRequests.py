import requests


def Get(url: str):
    print(url)
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
