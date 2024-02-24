import os.path
import pathlib

from PyQt6.QtCore import QSize, QRect, Qt
from PyQt6.QtWidgets import QDialog, QPushButton, QLabel, QProgressBar, QMessageBox

from src.core.requests.UrlGenerator import URL
from src.i18n import HistoryDialog as Strings
from src.core.requests.HistoryView import GetHistoryList
from src.core.requests.DownloadThread import DownloadThread
from src.core.requests.RequestThread import RequestData
from src.core.settings.FileSystemConfig import FileSystemConfig


class UI:
    WindowSize = QSize(400, 200)
    BtnNextGeo = QRect(250, 160, 20, 20)
    BtnPrevGeo = QRect(130, 160, 20, 20)
    LabelNumberGeo = QRect(140, 160, 120, 20)
    LabelDigest = QRect(20, 20, 360, 30)
    LabelTime = QRect(20, 60, 360, 30)
    BtnDownloadGeo = QRect(20, 100, 80, 25)
    ProgressGeo = QRect(20, 135, 360, 15)


class HistoryDialog(QDialog):
    def __init__(self, parent, user_name):
        super().__init__(parent)
        self.status_ready = parent.status_ready
        self.status_busy = parent.status_busy
        self.config = FileSystemConfig()
        self.download_thread = None
        self.user_name = user_name

        # Window appearance
        self.setWindowTitle(Strings.Window.Title.format(self.user_name))
        self.setFixedSize(UI.WindowSize)

        # Get the history list
        self.history_list = []
        self.history_idx = -1
        self.update_history()

        # Window Components
        self.m_label_number = QLabel(self)
        self.m_label_number.setGeometry(UI.LabelNumberGeo)
        self.m_label_number.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.m_btn_next = QPushButton(Strings.Pick.Next, self)
        self.m_btn_next.setGeometry(UI.BtnNextGeo)
        self.m_btn_next.clicked.connect(self.slot_page_next)

        self.m_btn_prev = QPushButton(Strings.Pick.Prev, self)
        self.m_btn_prev.setGeometry(UI.BtnPrevGeo)
        self.m_btn_prev.clicked.connect(self.slot_page_prev)

        self.m_label_digest = QLabel(self)
        self.m_label_digest.setGeometry(UI.LabelDigest)

        self.m_label_time = QLabel(self)
        self.m_label_time.setGeometry(UI.LabelTime)

        self.m_btn_download = QPushButton(Strings.Download.Text, self)
        self.m_btn_download.setGeometry(UI.BtnDownloadGeo)
        self.m_btn_download.clicked.connect(self.slot_download_start)

        self.m_progress = QProgressBar(self)
        self.m_progress.setGeometry(UI.ProgressGeo)

        # Launch the dialog
        self.update_button_status()
        self.exec()

    def update_history(self):
        def aux(response: RequestData):
            self.status_ready()
            if response.status_code == 200:
                lst = response.data
                self.history_list = sorted(lst, key=lambda x: x["time"], reverse=True)
                self.history_idx = 0 if len(lst) != 0 else -1
            else:
                QMessageBox.critical(self, "[History] Unhandled Error!", response.data["."])
            self.update_button_status()

        self.status_busy(Strings.Status.BusyUpdateHistory)
        GetHistoryList(aux, self.user_name)

    def update_button_status(self):
        total = len(self.history_list)
        if total == 0:
            self.m_btn_prev.setEnabled(False)
            self.m_btn_next.setEnabled(False)
        elif self.history_idx == 0:
            self.m_btn_prev.setEnabled(False)
            self.m_btn_next.setEnabled(True)
        elif self.history_idx == len(self.history_list) - 1:
            self.m_btn_prev.setEnabled(True)
            self.m_btn_next.setEnabled(False)
        else:
            self.m_btn_prev.setEnabled(True)
            self.m_btn_next.setEnabled(True)
        self.m_label_number.setText(Strings.Pick.Number.format(self.history_idx + 1, total))
        self.m_btn_download.setEnabled(total > 0)

        if self.history_idx > -1:
            self.m_label_digest.setText(Strings.Info.Digest.format(self.history_list[self.history_idx]["digest"]))
            self.m_label_time.setText(Strings.Info.Time.format(self.history_list[self.history_idx]["time"]))
        else:
            self.m_label_digest.clear()
            self.m_label_time.clear()

    def slot_page_next(self):
        self.history_idx += 1
        self.update_button_status()

    def slot_page_prev(self):
        self.history_idx -= 1
        self.update_button_status()

    def slot_download_start(self):
        self.m_progress.setValue(0)

        path = self.config.get_storage_path()
        if path.strip() == "" or not pathlib.Path(path).is_dir():
            QMessageBox.critical(self, Strings.WrongPath.Title, Strings.WrongPath.Content.format(path))
            return

        self.download_thread: DownloadThread = DownloadThread(
            URL.DownloadSource(self.history_list[self.history_idx]["digest"]),
            open(os.path.join(path, self.history_list[self.history_idx]["digest"] + ".zip"), "wb"), 1024
        )
        self.download_thread.sig_download_progress.connect(self.slot_progress_update)
        self.download_thread.start()

    def slot_progress_update(self, value: int):
        self.m_progress.setValue(value)
