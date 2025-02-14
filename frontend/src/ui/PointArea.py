import os
import pathlib

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox, QTextEdit, QGridLayout, QErrorMessage

from src.ui.ModifyDescDialog import ModifyDescDialog
from src.ui.PointIndexLabel import PointIndexLabel
from src.core.requests.SimpleQueryRequests import GetPointREMsg, SetPointStatus, SetPointDesc
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
        Disabled = QColor(150, 150, 150)


class PointArea(QWidget):
    sig_refresh_call = pyqtSignal()

    def __init__(self, idx, same_lst, diff_lst, desc, ret_desc,
                 user: str, proj: int, unit: int,
                 disabled: bool, status_fn):
        super().__init__()

        self.download_thread = None
        self.config = FileSystemConfig()

        self.user, self.proj, self.unit, self.point = user, proj, unit, idx
        self.disabled = disabled
        self.status_ready, self.status_busy = status_fn

        self.setAttribute(Qt.WidgetAttribute.WA_AlwaysShowToolTips)
        self.setMaximumHeight(UI.MaxHeight)

        self.m_layout_main = QGridLayout(self)
        self.m_layout_main.setColumnStretch(0, 1)
        self.m_layout_main.setColumnStretch(1, 7)
        self.m_layout_main.setColumnStretch(2, 5)
        self.m_layout_main.setColumnStretch(3, 5)
        self.m_layout_main.setColumnStretch(4, 10)
        self.m_layout_main.setColumnStretch(5, 5)
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

        self.m_btn_switch = QPushButton(Strings.Modify.Enable if disabled else Strings.Modify.Disable, self)
        self.m_btn_switch.clicked.connect(self.slot_set_disable(not disabled))
        self.m_layout_main.addWidget(self.m_btn_switch, 0, 5, 1, 1)

        self.m_btn_modify = QPushButton(Strings.Modify.ModifyDesc, self)
        self.m_btn_modify.clicked.connect(self.slot_modify_desc)
        self.m_layout_main.addWidget(self.m_btn_modify, 1, 5, 1, 1)

        self.m_btn_dict: {str, QPushButton} = {
            "input": QPushButton(Strings.Download.Input, self),
            "output": QPushButton(Strings.Download.Output, self),
            "all": QPushButton(Strings.Download.Others, self)
        }

        for scope in ["input", "output", "all"]:
            self.m_layout_main.addWidget(self.m_btn_dict[scope], *UI.BtnPos[scope])
            self.m_btn_dict[scope].clicked.connect(self.slot_common_download(scope))

        if disabled:
            self.m_label_idx.setBackgroundColor(UI.LabelColor.Disabled)
        # Judge Correct
        elif ret_desc == "Return Value: 0":
            if len(diff_lst) == 0:
                self.m_label_idx.setBackgroundColor(UI.LabelColor.Correct)
            else:
                self.m_label_idx.setBackgroundColor(UI.LabelColor.Diff)
        else:
            self.m_label_idx.setBackgroundColor(UI.LabelColor.Error)

    def slot_modify_desc(self):
        def handle_modify(new_desc):
            def aux(response: RequestData):
                if response.status_code == 200:
                    QMessageBox.information(self, "Okay!", str(response.data))
                else:
                    QMessageBox.critical(self, "[Requests Error]", str(response.data))
                self.sig_refresh_call.emit()

            SetPointDesc(aux, self.proj, self.unit, self.point, new_desc)

        modify_dlg = ModifyDescDialog(self, self.m_text.toHtml())
        modify_dlg.sig_done.connect(handle_modify)
        modify_dlg.exec()

    def slot_set_disable(self, disable):
        def ret():
            def aux(response: RequestData):
                if response.status_code == 200:
                    QMessageBox.information(self, "Okay!", str(response.data))
                else:
                    QMessageBox.critical(self, "[Requests Error]", str(response.data))
                self.sig_refresh_call.emit()

            SetPointStatus(aux, self.proj, self.unit, self.point, disable)
        return ret

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
