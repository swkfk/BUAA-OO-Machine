import typing

from PyQt6.QtCore import QSize, QRect, QUrl, Qt
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QTextEdit, QFileDialog, QLineEdit, QMessageBox, \
    QVBoxLayout, QHBoxLayout, QWidget

from src.core.fs.UploadThread import UploadThread
from src.i18n import UploadDialog as Strings


class UI:
    MinSize = QSize(200, 120)
    WinSize = QSize(400, 240)


class UploadDialog(QDialog):
    def __init__(self, parent, proj_id, proj, unit_id, unit):
        super().__init__(parent)

        self.upload_thread = None
        self.proj, self.unit = proj_id, unit_id
        self.setMinimumSize(UI.MinSize)
        self.resize(UI.WinSize)
        self.setWindowTitle(Strings.Window.Title)

        self.m_layout_main = QVBoxLayout(self)
        for r, s in [(0, 5), (1, 5), (2, 6), (3, 20)]:
            self.m_layout_main.setStretch(r, s)

        # Row 0
        self.m_label_proj = QLabel(Strings.Hint.Proj.format(proj), self)
        self.m_layout_main.addWidget(self.m_label_proj)

        # Row 1
        self.m_label_unit = QLabel(Strings.Hint.Unit.format(unit), self)
        self.m_layout_main.addWidget(self.m_label_unit)

        # Row 2
        self.m_widget_file = QWidget(self)
        self.m_layout_file = QHBoxLayout(self.m_widget_file)

        self.m_btn_file = QPushButton(Strings.File.Btn, self.m_widget_file)
        self.m_layout_file.addWidget(self.m_btn_file)

        self.m_line_file = QLineEdit(Strings.File.Unknown, self.m_widget_file)
        self.m_line_file.setReadOnly(True)
        self.m_layout_file.addWidget(self.m_line_file)

        self.m_widget_file.setLayout(self.m_layout_file)
        self.m_layout_main.addWidget(self.m_widget_file)

        self.m_layout_file.setStretch(0, 1)
        self.m_layout_file.setStretch(1, 3)

        # Row 3
        self.m_widget_desc = QWidget(self)
        self.m_layout_desc = QHBoxLayout(self.m_widget_desc)

        self.m_text_desc = QTextEdit(self.m_widget_desc)
        self.m_text_desc.setPlaceholderText(Strings.Desc.Label)
        self.m_layout_desc.addWidget(self.m_text_desc)

        self.m_widget_desc.setLayout(self.m_layout_desc)
        self.m_layout_main.addWidget(self.m_widget_desc)

        self.m_layout_desc.setStretch(0, 1)
        self.m_layout_desc.addStretch(1)

        # Fixed Button
        self.m_btn_confirm = QPushButton(Strings.Confirm.Btn, self)

        # Layout Finish
        self.setLayout(self.m_layout_main)

        # Bind Signals
        self.m_btn_file.clicked.connect(self.slot_choose_file)
        self.m_btn_confirm.clicked.connect(self.slot_confirm)

        self.exec()

    def slot_choose_file(self):
        u, _ = QFileDialog.getOpenFileUrl(self, Strings.File.Desc, QUrl("./"))
        file = u.toLocalFile()
        if not file == "":
            self.m_line_file.setText(file)

    def slot_confirm(self):
        def aux(s: str):
            self.m_btn_confirm.setText(Strings.Confirm.Btn)
            QMessageBox.information(self, Strings.Confirm.ResultTitle, s)
            self.close()

        self.m_btn_confirm.setText(Strings.Confirm.Uploading)
        self.upload_thread: UploadThread = UploadThread(
            self.proj, self.unit, self.m_line_file.text(), self.m_text_desc.toHtml()
        )
        self.upload_thread.sig_finish.connect(aux)
        self.upload_thread.start()

    def resizeEvent(self, a0: typing.Optional[QResizeEvent]) -> None:
        a0.accept()
        size = self.size()
        self.m_btn_confirm.setGeometry(size.width() - 100, size.height() - 30, 80, 20)
