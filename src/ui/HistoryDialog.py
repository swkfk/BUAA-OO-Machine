import os.path

from PyQt6.QtCore import QSize, QRect, Qt, QUrl
from PyQt6.QtWidgets import QDialog, QPushButton, QLabel, QProgressBar, QFileDialog

from src.strings.HistoryDialog import Strings
from src.core.requests.HistoryView import GetHistoryList
from src.core.requests.DownloadThread import DownloadThread


class UI:
    WindowSize = QSize(400, 200)
    BtnNextGeo = QRect(240, 160, 20, 20)
    BtnPrevGeo = QRect(140, 160, 20, 20)
    LabelNumberGeo = QRect(180, 160, 40, 20)
    LabelDigest = QRect(20, 20, 360, 30)
    LabelTime = QRect(20, 60, 360, 30)
    BtnDownloadGeo = QRect(20, 100, 80, 25)
    ProgressGeo = QRect(20, 135, 360, 15)


class HistoryDialog(QDialog):
    def __init__(self, parent, user_name):
        super().__init__(parent)
        self.download_thread = None
        self.user_name = user_name

        # Window appearance
        self.setWindowTitle(Strings.Window.Title.format(self.user_name))
        self.resize(UI.WindowSize)

        # Get the history list
        self.history_list = []
        self.history_idx = -1
        GetHistoryList(self.user_name, self.update_history_cb)

        # Window Components
        self.m_btn_next = QPushButton(Strings.Pick.Next, self)
        self.m_btn_next.setGeometry(UI.BtnNextGeo)
        self.m_btn_next.clicked.connect(self.slot_page_next)

        self.m_btn_prev = QPushButton(Strings.Pick.Prev, self)
        self.m_btn_prev.setGeometry(UI.BtnPrevGeo)
        self.m_btn_prev.clicked.connect(self.slot_page_prev)

        self.m_label_number = QLabel(self)
        self.m_label_number.setGeometry(UI.LabelNumberGeo)
        self.m_label_number.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

    def update_history_cb(self, lst: [{str: str}]):
        self.history_list = sorted(lst, key=lambda x: x["time"], reverse=True)
        self.history_idx = 0 if len(lst) != 0 else -1

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
        path = QFileDialog.getExistingDirectoryUrl(self, "", QUrl("./")).toLocalFile()
        if path == "":
            return

        self.download_thread: DownloadThread = DownloadThread(
            "https://mirrors.tuna.tsinghua.edu.cn/ctex/3.0/CTeX_3.0.215.2.exe",  # Just for test!
            open(os.path.join(path, self.history_list[self.history_idx]["digest"] + ".zip"), "wb"), 1024
        )
        self.download_thread.sig_download_progress.connect(self.slot_progress_update)
        self.download_thread.start()

    def slot_progress_update(self, value: int):
        self.m_progress.setValue(value)
