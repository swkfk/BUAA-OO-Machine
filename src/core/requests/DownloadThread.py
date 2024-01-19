import requests
from PyQt6.QtCore import QThread, pyqtSignal


class DownloadThread(QThread):
    sig_download_progress = pyqtSignal(int)

    def __init__(self, url, file_obj, buf_size):
        super().__init__()
        self.url = url
        self.resp = requests.get(self.url, stream=True)
        self.file_size: str = self.resp.headers['Content-Length']
        self.file_obj = file_obj
        self.buf_size = buf_size

    def run(self):
        try:
            offset = 0
            for chunk in self.resp.iter_content(chunk_size=self.buf_size):
                self.file_obj.seek(offset)
                self.file_obj.write(chunk)
                offset += len(chunk)
                progress = offset / int(self.file_size)
                self.sig_download_progress.emit(int(progress * 100))
            self.file_obj.close()
            self.exit(0)
        except Exception as e:
            print(repr(e))
