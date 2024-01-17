from PyQt6.QtCore import QRect, QSize, Qt
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton

from src.strings.PointArea import Strings


class UI:
    Size = QSize(740, 80)
    IdxGeo = QRect(0, 0, 60, 30)
    SameGeo = QRect(0, 30, 100, 30)
    DiffGeo = QRect(100, 30, 100, 30)

    BtnInGeo = QRect(200, 0, 80, 30)
    BtnOutGeo = QRect(280, 0, 80, 30)
    BtnOtherGeo = QRect(200, 30, 160, 30)


class PointArea(QWidget):
    def __init__(self, idx, same_lst, diff_lst):
        super().__init__()

        self.setFixedSize(UI.Size)
        self.setAttribute(Qt.WidgetAttribute.WA_AlwaysShowToolTips)

        self.m_label_idx = QLabel(Strings.Widget.Index.format(idx), self)
        self.m_label_idx.setGeometry(UI.IdxGeo)

        self.m_label_same = QLabel(Strings.Widget.Same.format(len(same_lst)), self)
        self.m_label_same.setGeometry(UI.SameGeo)
        self.m_label_same.setToolTip(Strings.Widget.ToolTip(same_lst))

        self.m_label_diff = QLabel(Strings.Widget.Diff.format(len(diff_lst)), self)
        self.m_label_diff.setGeometry(UI.DiffGeo)
        self.m_label_diff.setToolTip(Strings.Widget.ToolTip(diff_lst))

        self.m_btn_input = QPushButton(Strings.Download.Input, self)
        self.m_btn_input.setGeometry(UI.BtnInGeo)

        self.m_btn_output = QPushButton(Strings.Download.Output, self)
        self.m_btn_output.setGeometry(UI.BtnOutGeo)

        self.m_btn_others = QPushButton(Strings.Download.Others, self)
        self.m_btn_others.setGeometry(UI.BtnOtherGeo)

