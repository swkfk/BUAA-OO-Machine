from typing import Any

import requests
from PyQt6.QtCore import QThread, pyqtSignal


class RequestData:
    status_code: int
    data: Any


class RequestThread(QThread):
    sig_request_response = pyqtSignal(RequestData)

    def __init__(self, url, *args, **kwargs):
        super().__init__()
        self.url = url
        self.args = args
        self.kwargs = kwargs

    def run(self) -> None:
        dat = RequestData()
        try:
            req = requests.get(self.url, *self.args, timeout=(5, 5),  **self.kwargs)
            dat.status_code = req.status_code
            dat.data = req.json()
        except requests.ConnectTimeout as e:
            dat.status_code = 0
            dat.data = {".": "Connection Timeout!"}
        except Exception as e:
            dat.status_code = -1
            dat.data = {".": repr(e)}
        self.sig_request_response.emit(dat)
