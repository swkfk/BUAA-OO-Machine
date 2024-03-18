from time import sleep

import websocket
from PyQt6.QtCore import QThread, pyqtSignal

from src.core.fs.Zip import compress
from src.core.requests.SubmitOperation import get_status, submit
from src.core.requests.UrlGenerator import URL
from src.core.settings.FileSystemConfig import FileSystemConfig


class SubmitThread(QThread):
    sig_status_update = pyqtSignal(str)
    sig_get_digest = pyqtSignal(str)

    def __init__(self, user: str, proj: int, unit: int, main_class: str):
        super().__init__()
        self.fs_config = FileSystemConfig()
        self.user, self.proj, self.unit, self.main_class = user, proj, unit, main_class

    def run(self):
        # Tar the source files
        sleep(0.3)
        obj = compress(self.fs_config.get_src_path(), self.fs_config.get_zip_passwd())
        self.sig_status_update.emit("Zipped")

        # Submit the zip file
        sleep(0.5)
        digest = submit(self.user, self.proj, self.unit, self.main_class, self.fs_config.get_zip_passwd(), obj)

        if type(digest) != str or digest.startswith("-"):
            print("Bad Digest: ", digest)  # TODO: Error handler
            return
        self.sig_get_digest.emit(digest)
        ws = websocket.WebSocket()
        ws.connect(URL.StatusWs(digest))
        status = ws.recv()
        self.sig_status_update.emit(status)
        assert (status == "Submitted"), f"Invalid Socket Msg: {status}"

        # Poll the status
        while status != "Done" and not status.startswith("Err"):
            status = ws.recv()
            self.sig_status_update.emit(status)
        ws.send_close()
