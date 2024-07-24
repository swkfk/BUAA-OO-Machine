import requests

from src.core.requests.RequestThread import RequestThread

lst = []  # An Expedient Solution


def callback_handler(aux, *args, **kwargs):
    th = RequestThread(*args, **kwargs)
    lst.append(th)
    th.sig_request_response.connect(aux)
    th.start()


def raw_get(url):
    return requests.get(url, timeout=(5, 5))


def raw_file_post(url, files):
    return requests.post(url, timeout=(10, 5), files=files)
