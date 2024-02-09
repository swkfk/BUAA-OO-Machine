import requests

from src.core.fs.TempFile import TempFile
from src.core.requests.CommonRequests import raw_get, raw_file_post
from src.core.requests.UrlGenerator import URL


def get_status(digest: str):
    try:
        return raw_get(URL.Status(digest)).json()
    except requests.Timeout:
        return "Timeout"
    except Exception as e:
        return repr(e)


def submit(user: str, proj: int, unit: int, tf: TempFile):
    try:
        return raw_file_post(URL.Submit(user, proj, unit), files={"file": (tf.name(), tf.obj().read())}).json()
    except requests.Timeout:
        return "-: Timeout"
    except Exception as e:
        return "-: " + repr(e)
