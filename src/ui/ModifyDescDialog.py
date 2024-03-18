from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QDialog, QTextEdit, QGridLayout, QPushButton

from src.i18n import PointArea as Strings

class ModifyDescDialog(QDialog):
    sig_done = pyqtSignal(str)

    def __init__(self, parent, html):
        super().__init__(parent)

        self.setWindowTitle(Strings.ModifyDialog.Title)

        self.m_layout_main = QGridLayout(self)
        self.m_layout_main.setRowStretch(0, 8)
        self.m_layout_main.setRowStretch(1, 1)

        self.m_text_edit = QTextEdit(self)
        self.m_text_edit.setHtml(html)
        self.m_layout_main.addWidget(self.m_text_edit, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        self.m_btn_ok = QPushButton(Strings.ModifyDialog.Ok, self)
        self.m_btn_ok.setMinimumWidth(40)
        self.m_btn_ok.clicked.connect(self.slot_ok)
        self.m_layout_main.addWidget(self.m_btn_ok, 1, 0, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.m_btn_cancel = QPushButton(Strings.ModifyDialog.Cancel, self)
        self.m_btn_cancel.setMinimumWidth(40)
        self.m_btn_cancel.clicked.connect(self.slot_cancel)
        self.m_layout_main.addWidget(self.m_btn_cancel, 1, 1, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.setLayout(self.m_layout_main)

    def slot_ok(self):
        self.sig_done.emit(self.m_text_edit.toHtml())
        self.done(0)

    def slot_cancel(self):
        self.done(1)
