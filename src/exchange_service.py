import requests

from functools import lru_cache

from requests.adapters import HTTPAdapter


session = requests.Session()

adapter = HTTPAdapter(max_retries=3)

session.mount("https://", adapter)


@lru_cache(maxsize=1)
def get_usd_rate():

    url = "https://open.er-api.com/v6/latest/INR"

    response = session.get(url, timeout=10)

    response.raise_for_status()

    data = response.json()

    return data["rates"]["USD"]