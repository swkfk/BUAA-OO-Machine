import base64
import random
import string

import requests

from src.core.Encipher import Encipher
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


def submit(user: str, proj: int, unit: int, main_class: str, passwd: str, tf: TempFile):
    try:
        class_base64 = base64.urlsafe_b64encode(main_class.encode('utf-8')).decode('utf-8')
        if passwd == "":
            return raw_file_post(
                URL.Submit(user, proj, unit, class_base64),
                files={"file": (tf.name(), tf.obj().read())}
            ).json()
        salt = "".join(random.choices(string.ascii_letters, k=random.randint(10, 20)))
        return raw_file_post(
            URL.Submit(user, proj, unit, class_base64, Encipher(passwd, salt, user), salt),
            files={"file": (tf.name(), tf.obj().read())}
        ).json()
    except requests.Timeout:
        return "-: Timeout"
    except Exception as e:
        return "-: " + repr(e)


def get_ce_msg(digest: str) -> str:
    try:
        text = raw_get(URL.CEMsg(digest)).text.replace(r"\n", '<br/>').removeprefix('"').removesuffix('"')
        text = "<pre>" + text + "</pre>"
        return text
    except requests.Timeout:
        return "[Request Timeout]"
    except Exception as e:
        return repr(e)
