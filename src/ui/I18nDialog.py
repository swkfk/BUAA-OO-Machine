from functools import partial

from PyQt6.QtCore import QSize, QRect
from PyQt6.QtWidgets import QDialog, QPushButton

from src.core.settings.I18nConfig import set_lang
from src.i18n import lang_list


class UI:
    def __init__(self, cnt):
        self.cnt = cnt

    def Size(self):
        return QSize(110 * self.cnt + 340, 250)

    @staticmethod
    def I_thGeo(i):
        return QRect(170 + i * 110, 105, 100, 40)


class I18nDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = UI(len(lang_list))

        self.setWindowTitle(" ")
        self.setFixedSize(self.ui.Size())

        self.btn_lst = []
        for i, (code, text) in enumerate(lang_list):
            btn = QPushButton(text, self)
            btn.setGeometry(self.ui.I_thGeo(i))
            btn.clicked.connect(partial(lambda x: set_lang(x) is not None or self.deleteLater(), code))
            self.btn_lst.append(btn)

        self.exec()
