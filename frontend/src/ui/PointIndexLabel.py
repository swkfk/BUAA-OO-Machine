import typing

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QMouseEvent, QColor, QPaintEvent, QPainter, QPen, QFontMetrics
from PyQt6.QtWidgets import QLabel, QWidget


class PointIndexLabel(QLabel):
    clicked = pyqtSignal()

    @typing.overload
    def __init__(self, text: str, parent: QWidget) -> None: ...

    @typing.overload
    def __init__(self, parent: QWidget) -> None: ...

    def __init__(self, *args):
        super().__init__(*args)
        self.background_color = None

    def mouseReleaseEvent(self, ev: QMouseEvent):
        self.clicked.emit()

    def click(self):
        self.clicked.emit()

    def setBackgroundColor(self, background_color: QColor):
        self.background_color = background_color

    def paintEvent(self, a0: typing.Optional[QPaintEvent]) -> None:
        painter = QPainter(self)
        pen = QPen()

        pen.setColor(self.background_color)
        painter.setPen(pen)
        painter.fillRect(self.rect(), self.background_color)

        pen.setColor(QColor(0, 0, 0))
        painter.setPen(pen)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
