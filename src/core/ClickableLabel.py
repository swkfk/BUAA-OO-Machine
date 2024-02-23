import typing

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QLabel, QWidget


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    @typing.overload
    def __init__(self, text: str, parent: QWidget) -> None: ...

    @typing.overload
    def __init__(self, parent: QWidget) -> None: ...

    def __init__(self, *args):
        super().__init__(*args)

    def mouseReleaseEvent(self, ev: QMouseEvent):
        self.clicked.emit()

    def click(self):
        self.clicked.emit()
