from PyQt6.QtCore import QSize, QRect, Qt
from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QApplication, QStyle

from src.strings.RegisterDialog import Strings


class UI:
    DialogSize = QSize(300, 600)
    InputPromptGeo = QRect(20, 80, 260, 80)
    InputBoxGeo = QRect(60, 160, 180, 40)
    InputButtonGeo = QRect(120, 300, 60, 20)


class RegisterDialog(QDialog):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback

        # Window Appearance
        self.setWindowTitle(Strings.Window.Title)
        self.setFixedSize(UI.DialogSize)

        # Setup UI
        self.m_label_input = QLabel(Strings.Input.Prompt, self)
        self.m_label_input.setGeometry(UI.InputPromptGeo)
        self.m_label_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.m_input = QLineEdit(self)
        self.m_input.setGeometry(UI.InputBoxGeo)
        self.m_input.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # self.m_btn_input = QLabel(self)
        # style = QApplication.style()
        # self.m_btn_input.setPixmap(style.standardPixmap(style.StandardPixmap.SP_ArrowForward).scaled(32, 32))

        self.m_btn_input = QPushButton(Strings.Input.Button, self)
        self.m_btn_input.setGeometry(UI.InputButtonGeo)
        self.m_btn_input.clicked.connect(self.button_clicked)

        # Launch the dialog
        self.exec()

    def button_clicked(self):
        user_name = self.m_input.text()
        self.callback(user_name)
        self.deleteLater()
