import os
import pathlib

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox, QTextEdit, QGridLayout, QErrorMessage

from src.ui.PointIndexLabel import PointIndexLabel
from src.core.requests.SimpleQueryRequests import GetPointREMsg
from src.core.requests.DownloadThread import DownloadThread
from src.core.requests.RequestThread import RequestData
from src.core.requests.UrlGenerator import URL
from src.core.settings.FileSystemConfig import FileSystemConfig
from src.i18n import PointArea as Strings


class UI:
    MaxHeight = 80

    BtnPos = {
        "input": (0, 2, 1, 1),
        "output": (0, 3, 1, 1),
        "all": (1, 2, 1, 2)
    }

    class LabelColor:
        Correct = QColor(255, 255, 128)
        Diff = QColor(128, 128, 255)
        Error = QColor(255, 36, 36)


class PointArea(QWidget):
    def __init__(self, idx, same_lst, diff_lst, desc, ret_desc, user: str, proj: int, unit: int, status_fn):
        super().__init__()

        self.download_thread = None
        self.config = FileSystemConfig()

        self.user, self.proj, self.unit, self.point = user, proj, unit, idx
        self.status_ready, self.status_busy = status_fn

        self.setAttribute(Qt.WidgetAttribute.WA_AlwaysShowToolTips)
        self.setMaximumHeight(UI.MaxHeight)

        self.m_layout_main = QGridLayout(self)
        self.m_layout_main.setColumnStretch(0, 1)
        self.m_layout_main.setColumnStretch(1, 7)
        self.m_layout_main.setColumnStretch(2, 5)
        self.m_layout_main.setColumnStretch(3, 5)
        self.m_layout_main.setColumnStretch(4, 10)
        self.setLayout(self.m_layout_main)

        self.m_label_idx = PointIndexLabel(Strings.Widget.Index.format(idx), self)
        self.m_label_idx.clicked.connect(self.slot_request_re_msg)
        self.m_label_idx.setToolTip(ret_desc)
        self.m_layout_main.addWidget(self.m_label_idx, 0, 0, 2, 1, Qt.AlignmentFlag.AlignCenter)

        self.m_label_same = QLabel(Strings.Widget.Same.format(len(same_lst)), self)
        self.m_label_same.setToolTip(Strings.Widget.ToolTip(same_lst))
        self.m_layout_main.addWidget(self.m_label_same, 0, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.m_label_diff = QLabel(Strings.Widget.Diff.format(len(diff_lst)), self)
        self.m_label_diff.setToolTip(Strings.Widget.ToolTip(diff_lst))
        self.m_layout_main.addWidget(self.m_label_diff, 1, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.m_text = QTextEdit(desc, self)
        self.m_text.setReadOnly(True)
        self.m_layout_main.addWidget(self.m_text, 0, 4, 2, 1, Qt.AlignmentFlag.AlignCenter)

        self.m_btn_dict: {str, QPushButton} = {
            "input": QPushButton(Strings.Download.Input, self),
            "output": QPushButton(Strings.Download.Output, self),
            "all": QPushButton(Strings.Download.Others, self)
        }

        for scope in ["input", "output", "all"]:
            self.m_layout_main.addWidget(self.m_btn_dict[scope], *UI.BtnPos[scope])
            self.m_btn_dict[scope].clicked.connect(self.slot_common_download(scope))

        # Judge Correct
        if ret_desc == "Return Value: 0":
            if len(diff_lst) == 0:
                self.m_label_idx.setBackgroundColor(UI.LabelColor.Correct)
            else:
                self.m_label_idx.setBackgroundColor(UI.LabelColor.Diff)
        else:
            self.m_label_idx.setBackgroundColor(UI.LabelColor.Error)

    def slot_request_re_msg(self):
        def aux(response: RequestData):
            self.status_ready()
            if response.status_code == 200:
                error_dlg = QErrorMessage(self)
                error_dlg.setWindowTitle(Strings.MsgBox.RE_Title)
                error_dlg.showMessage(response.data)
            else:
                QMessageBox.critical(self, "[Requests Error]", response.data)

        self.status_busy(Strings.Bar.ReadMsg)
        GetPointREMsg(aux, self.user, self.proj, self.unit, self.point)

    def slot_common_download(self, scope: str):
        def aux():
            self.m_btn_dict[scope].setText(Strings.Bar.Download)
            self.status_busy(Strings.Bar.Download)

            path = self.config.get_storage_path()
            if path.strip() == "" or not pathlib.Path(path).is_dir():
                QMessageBox.critical(self, Strings.WrongPath.Title, Strings.WrongPath.Content.format(path))
                self.m_btn_dict[scope].setText(Strings.Download.Dict[scope])
                self.status_ready()
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
