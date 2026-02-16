from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import requests

def get_parameters(url):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    return params


def inject_param(url, param_name, payload):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    params[param_name] = payload

    new_query = urlencode(params, doseq=True)

    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))

    r = requests.get(new_url, timeout=5)

    return r.text, new_url