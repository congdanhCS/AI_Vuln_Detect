import requests

def inject(endpoint, payload):

    data = {field: payload for field in endpoint["inputs"]}

    if endpoint["method"].lower() == "post":
        r = requests.post(endpoint["url"], data=data, timeout=5)
    else:
        r = requests.get(endpoint["url"], params=data, timeout=5)

    return r.text