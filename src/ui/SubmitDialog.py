from PyQt6.QtCore import QSize, QRect, Qt
from PyQt6.QtWidgets import QDialog, QLabel, QHBoxLayout, QRadioButton, QWidget

from src.core.fs.SubmitThread import SubmitThread
from src.i18n import SubmitDialog as Strings


class UI:
    WindowSize = QSize(400, 140)
    HintGeo = QRect(20, 20, 360, 30)
    BubbleGeo = QRect(100, 80, 200, 40)


class SubmitDialog(QDialog):
    def __init__(self, parent, user, proj, unit):
        super().__init__(parent)

        self.th_submit = SubmitThread(user, proj, unit)
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
            print(f"Unhandled Status: {s}")
            index = -1  # TODO: Handle this
            # QMessageBox.critical(self, "Unknown Exception!", f"Unknown Status: {s}\n{repr(e)}")
            # return
        self.m_label_hint.setText(Strings.Status.Hint[index])
        for i in range(5):
            self.m_btn_bubble[i].setChecked(i <= index)

    def slot_set_digest(self, s: str):
        self.setWindowTitle(Strings.Window.Title.format(s))
