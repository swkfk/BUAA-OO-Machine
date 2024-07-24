import base64

from PyQt6.QtCore import QThread, pyqtSignal

from src.core.requests.UploadOperation import upload
from src.core.settings.FileSystemConfig import FileSystemConfig


class UploadThread(QThread):
    sig_finish = pyqtSignal(str)

    def __init__(self, proj: int, unit: int, path: str, desc: str):
        super().__init__()
        self.fs_config = FileSystemConfig()
        self.proj, self.unit, self.path, self.desc = proj, unit, path, desc

    def run(self):
        desc_base64 = base64.urlsafe_b64encode(self.desc.encode('utf-8')).decode('utf-8')
        # TODO /// Error Handler
        self.sig_finish.emit(upload(self.proj, self.unit, desc_base64, open(self.path, 'rb')))
