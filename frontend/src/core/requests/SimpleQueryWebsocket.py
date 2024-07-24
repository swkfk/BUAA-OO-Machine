import websocket
from PyQt6.QtCore import QThread, pyqtSignal

from src.core.requests.UrlGenerator import URL

lst = []

def GetPointStatusWs(callback, handle_fi, user_name: str, proj_id: int, unit_id: int):
    class _Thread(QThread):
        sig_update = pyqtSignal(str)
        sig_over = pyqtSignal()

        def run(self) -> None:
            ws = websocket.WebSocket()
            ws.connect(URL.PointListWs(user_name, proj_id, unit_id))
            ws.send_text(user_name)
            count = int(ws.recv())
            self.sig_update.emit(f"0 / {count}")
            while True:
                self.msleep(10)  # How dare it???
                curr = int(ws.recv())
                if curr == -1:
                    break
                self.sig_update.emit(f"{curr} / {count}")
            ws.close()
            self.sig_over.emit()

    _thread = _Thread()
    _thread.sig_update.connect(callback)
    _thread.sig_over.connect(handle_fi)
    lst.append(_thread)
    _thread.start()
