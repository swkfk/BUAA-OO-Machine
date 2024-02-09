import os

from PyQt6.QtCore import QRect, QSize, Qt
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox

from src.core.requests.DownloadThread import DownloadThread
from src.core.requests.UrlGenerator import URL
from src.core.settings.FileSystemConfig import FileSystemConfig
from src.strings.PointArea import Strings


class UI:
    Size = QSize(740, 80)
    IdxGeo = QRect(0, 0, 60, 30)
    SameGeo = QRect(0, 30, 100, 30)
    DiffGeo = QRect(100, 30, 100, 30)

    BtnInGeo = QRect(200, 0, 80, 30)
    BtnOutGeo = QRect(280, 0, 80, 30)
    BtnOtherGeo = QRect(200, 30, 160, 30)


class PointArea(QWidget):
    def __init__(self, idx, same_lst, diff_lst, user: str, proj: int, unit: int, status_fn):
        super().__init__()

        self.download_thread = None
        self.config = FileSystemConfig()

        self.user, self.proj, self.unit, self.point = user, proj, unit, idx
        self.status_ready, self.status_busy = status_fn

        self.setFixedSize(UI.Size)
        self.setAttribute(Qt.WidgetAttribute.WA_AlwaysShowToolTips)

        self.m_label_idx = QLabel(Strings.Widget.Index.format(idx), self)
        self.m_label_idx.setGeometry(UI.IdxGeo)

        self.m_label_same = QLabel(Strings.Widget.Same.format(len(same_lst)), self)
        self.m_label_same.setGeometry(UI.SameGeo)
        self.m_label_same.setToolTip(Strings.Widget.ToolTip(same_lst))

        self.m_label_diff = QLabel(Strings.Widget.Diff.format(len(diff_lst)), self)
        self.m_label_diff.setGeometry(UI.DiffGeo)
        self.m_label_diff.setToolTip(Strings.Widget.ToolTip(diff_lst))

        self.m_btn_dict: {str, QPushButton} = {
            "input": QPushButton(Strings.Download.Input, self),
            "output": QPushButton(Strings.Download.Output, self),
            "all": QPushButton(Strings.Download.Others, self)
        }

        self.m_btn_dict["input"].setGeometry(UI.BtnInGeo)
        self.m_btn_dict["output"].setGeometry(UI.BtnOutGeo)
        self.m_btn_dict["all"].setGeometry(UI.BtnOtherGeo)

        for scope in ["input", "output", "all"]:
            self.m_btn_dict[scope].clicked.connect(self.slot_common_download(scope))

    def slot_common_download(self, scope: str):
        def aux():
            self.m_btn_dict[scope].setText(Strings.Bar.Download)
            self.status_busy(Strings.Bar.Download)

            path = self.config.get_storage_path()
            if path == "":
                return
            url = URL.DownloadInout(scope, self.user, self.proj, self.unit, self.point)
            suffix = "zip" if scope == "all" else "txt"
            path = os.path.join(
                path, f"{self.user}$P{self.proj}$U{self.unit}$Test_{self.point}_{scope}.{suffix}"
            )

            self.download_thread = DownloadThread(url, open(path, "wb"), 1024)

            def download_down():
                self.m_btn_dict[scope].setText(Strings.Download.Dict[scope])
                self.status_ready()
                QMessageBox.information(self, Strings.MsgBox.Title, Strings.MsgBox.Content.format(path))

            self.download_thread.sig_download_over.connect(download_down)
            self.download_thread.start()

        return aux
