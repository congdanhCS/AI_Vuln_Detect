import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl(url):
    endpoints = []

    r = requests.get(url, timeout=5)
    soup = BeautifulSoup(r.text, "html.parser")

    for form in soup.find_all("form"):
        action = form.get("action")
        method = form.get("method", "get")

        inputs = []
        for i in form.find_all("input"):
            if i.get("name"):
                inputs.append(i.get("name"))

        endpoints.append({
            "url": urljoin(url, action),
            "method": method,
            "inputs": inputs
        })

    return endpoints