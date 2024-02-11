from typing import IO

import requests

from src.core.requests.CommonRequests import raw_file_post
from src.core.requests.UrlGenerator import URL


def upload(proj: int, unit: int, desc_base64: str, file: IO):
    try:
        return raw_file_post(URL.Upload(proj, unit, desc_base64), files={"file": (file.name, file.read())}).json()
    except requests.Timeout:
        return "Timeout!"
    except Exception as e:
        return repr(e)
