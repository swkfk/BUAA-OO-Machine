from time import sleep

from PyQt6.QtCore import QThread, pyqtSignal

from src.core.fs.Zip import compress
from src.core.requests.SubmitOperation import get_status, submit
from src.core.settings.FileSystemConfig import FileSystemConfig


class SubmitThread(QThread):
    sig_status_update = pyqtSignal(str)
    sig_get_digest = pyqtSignal(str)

    def __init__(self, user: str, proj: int, unit: int):
        super().__init__()
        self.fs_config = FileSystemConfig()
        self.user, self.proj, self.unit = user, proj, unit

    def run(self):
        # Tar the source files
        sleep(0.3)
        obj = compress(self.fs_config.get_src_path())
        self.sig_status_update.emit("Zipped")

        # Submit the zip file
        sleep(0.5)
        digest = submit(self.user, self.proj, self.unit, obj)

        if type(digest) != str or digest.startswith("-"):
            print("Bad Digest: ", digest)  # TODO: Error handler
            return
        self.sig_status_update.emit("Submitted")
        self.sig_get_digest.emit(digest)

        # Poll the status
        status = "Submitted"
        while status != "Done":
            sleep(0.7)
            status = get_status(digest)
            self.sig_status_update.emit(status)
