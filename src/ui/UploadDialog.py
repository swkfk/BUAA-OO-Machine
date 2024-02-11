from PyQt6.QtCore import QSize, QRect, QUrl
from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QTextEdit, QFileDialog, QLineEdit

from src.strings.UploadDialog import Strings


class UI:
    WinSize = QSize(300, 170)

    LabelProjGeo = QRect(10, 10, 280, 20)
    LabelUnitGeo = QRect(10, 30, 280, 20)

    BtnFileGeo = QRect(10, 55, 80, 20)
    LineFileGeo = QRect(95, 55, 195, 20)

    LabelDescGeo = QRect(10, 80, 280, 20)
    TextDescGeo = QRect(10, 100, 140, 60)

    BtnConfirmGeo = QRect(210, 140, 80, 20)


class UploadDialog(QDialog):
    def __init__(self, parent, proj_id, proj, unit_id, unit):
        super().__init__(parent)

        self.resize(UI.WinSize)
        self.setWindowTitle(Strings.Window.Title)

        self.m_label_proj = QLabel(Strings.Hint.Proj.format(proj), self)
        self.m_label_proj.setGeometry(UI.LabelProjGeo)

        self.m_label_unit = QLabel(Strings.Hint.Unit.format(unit), self)
        self.m_label_unit.setGeometry(UI.LabelUnitGeo)

        self.m_btn_file = QPushButton(Strings.File.Btn, self)
        self.m_btn_file.setGeometry(UI.BtnFileGeo)

        self.m_line_file = QLineEdit(Strings.File.Unknown, self)
        self.m_line_file.setGeometry(UI.LineFileGeo)
        self.m_line_file.setReadOnly(True)

        self.m_label_desc = QLabel(Strings.Desc.Label, self)
        self.m_label_desc.setGeometry(UI.LabelDescGeo)

        self.m_text_desc = QTextEdit(self)
        self.m_text_desc.setGeometry(UI.TextDescGeo)

        self.m_btn_confirm = QPushButton(Strings.Confirm.Btn, self)
        self.m_btn_confirm.setGeometry(UI.BtnConfirmGeo)

        self.m_btn_file.clicked.connect(self.slot_choose_file)

        self.exec()

    def slot_choose_file(self):
        u, _ = QFileDialog.getOpenFileUrl(self, Strings.File.Desc, QUrl("./"))
        file = u.toLocalFile()
        if not file == "":
            self.m_line_file.setText(file)
