import pathlib

from PyQt6.QtCore import QSize, QRect, Qt
from PyQt6.QtWidgets import QDialog, QLabel, QHBoxLayout, QRadioButton, QWidget, QLineEdit, QPushButton, \
    QErrorMessage, QMessageBox

from src.core.fs.SubmitThread import SubmitThread
from src.core.requests.SubmitOperation import get_ce_msg
from src.core.settings.FileSystemConfig import FileSystemConfig
from src.core.settings.JavaConfig import get_main_class, set_main_class, set_not_ask_each, get_ask_each
from src.i18n import SubmitDialog as Strings


class UI:
    WindowSize = QSize(400, 140)
    HintGeo = QRect(20, 20, 360, 30)
    BubbleGeo = QRect(100, 80, 200, 40)

    AskSize = QSize(300, 110)
    AskInputGeo = QRect(20, 20, 260, 30)
    AskConfirmGeo = QRect(20, 70, 40, 25)
    AskNoAskGeo = QRect(65, 70, 120, 25)
    AskCancelGeo = QRect(240, 70, 40, 25)


class AskMainClassDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setFixedSize(UI.AskSize)
        self.setWindowTitle(Strings.Ask.Title)

        self.m_input = QLineEdit(get_main_class(), self)
        self.m_input.setGeometry(UI.AskInputGeo)
        self.m_input.textChanged.connect(set_main_class)

        self.m_btn_confirm = QPushButton(Strings.Ask.Confirm, self)
        self.m_btn_confirm.setGeometry(UI.AskConfirmGeo)
        self.m_btn_confirm.clicked.connect(lambda: self.done(QDialog.DialogCode.Accepted))

        self.m_btn_cancel = QPushButton(Strings.Ask.Cancel, self)
        self.m_btn_cancel.setGeometry(UI.AskCancelGeo)
        self.m_btn_cancel.clicked.connect(lambda: self.done(QDialog.DialogCode.Rejected))

        self.m_btn_no_ask = QPushButton(Strings.Ask.NoAskMore, self)
        self.m_btn_no_ask.setGeometry(UI.AskNoAskGeo)
        self.m_btn_no_ask.clicked.connect(
            lambda: self.done(QDialog.DialogCode.Accepted) is not None or set_not_ask_each()
        )


class SubmitDialog(QDialog):
    def __init__(self, parent, user, proj, unit):
        super().__init__(parent)

        src_path = FileSystemConfig().get_src_path()
        if src_path.strip() == "" or not pathlib.Path(src_path).is_dir():
            self.done(QDialog.DialogCode.Rejected)
            QMessageBox.critical(parent, Strings.WrongPath.Title, Strings.WrongPath.Content.format(src_path))
            return

        self.digest = ""
        if get_ask_each():
            dialog = AskMainClassDialog(parent)
            if QDialog.DialogCode.Rejected == dialog.exec():
                self.done(QDialog.DialogCode.Rejected)
                return

        self.th_submit = SubmitThread(user, proj, unit, get_main_class())
        self.th_submit.sig_get_digest.connect(self.slot_set_digest)
        self.th_submit.sig_status_update.connect(self.slot_update_status)

        self.setWindowTitle(Strings.Window.Title.format(Strings.Window.Wait))
        self.resize(UI.WindowSize)

        self.m_label_hint = QLabel(Strings.Status.Zipping, self)
        self.m_label_hint.setGeometry(UI.HintGeo)
        self.m_label_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.m_widget_bubble = QWidget(self)
        self.m_widget_bubble.setGeometry(UI.BubbleGeo)
        self.m_layout_bubble = QHBoxLayout(self.m_widget_bubble)

        self.m_btn_bubble = []
        for _ in range(5):
            btn = QRadioButton(self.m_widget_bubble)
            btn.setAutoExclusive(False)
            btn.setEnabled(False)
            self.m_btn_bubble.append(btn)
            self.m_layout_bubble.addWidget(btn)

        self.m_widget_bubble.setLayout(self.m_layout_bubble)
        self.m_widget_bubble.show()

        self.th_submit.start()
        self.exec()

    def slot_update_status(self, s: str):
        try:
            index = ["Zipped", "Submitted", "Unzipped", "Compiled", "Done"].index(s)
        except ValueError as e:
            index = -1
            if s == "Err::CE":
                # Compile Error
                error_dlg = QErrorMessage(self)
                error_dlg.setWindowTitle(Strings.Status.CE_Title)
                error_dlg.showMessage(get_ce_msg(self.digest))
            if s == "Err::RE":
                # Runtime Error
                error_dlg = QErrorMessage(self)
                error_dlg.setWindowTitle(Strings.Status.RE_Title)
                error_dlg.showMessage(Strings.Status.RE_Content)
            if s.startswith("("):
                self.m_label_hint.setText(self.m_label_hint.text() + " " + s)
                index = 3
            # QMessageBox.critical(self, "Unknown Exception!", f"Unknown Status: {s}\n{repr(e)}")
            # return
        self.m_label_hint.setText(Strings.Status.Hint[index] + (s if s.startswith("(") else ""))
        for i in range(5):
            self.m_btn_bubble[i].setChecked(i <= index)

    def slot_set_digest(self, s: str):
        self.digest = s
        self.setWindowTitle(Strings.Window.Title.format(s))
