import sys

from PyQt6.QtCore import QSize, QRect, QCoreApplication, QProcess
from PyQt6.QtWidgets import QWidget, QPushButton, QComboBox

from src.ui.RegisterDialog import RegisterDialog
from src.ui.HistoryDialog import HistoryDialog
from src.core.settings import LocalAuthentic
from src.strings.MainWidget import Strings


class UI:
    WindowSize = QSize(800, 600)

    UserBtnGeo = QRect(20, 20, 100, 30)
    ProjComboGeo = QRect(140, 20, 100, 30)
    UnitComboGeo = QRect(260, 20, 100, 30)
    SyncBtnGeo = QRect(560, 20, 100, 30)
    UploadDataBtnGeo = QRect(680, 20, 100, 30)

    HistoryBtnGeo = QRect(560, 60, 100, 30)
    SubmitBtnGeo = QRect(680, 60, 100, 30)


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.user = LocalAuthentic.User()
        if self.user.status() == self.user.UserStatus.NONE:
            RegisterDialog(self, self.user.create_user)

        self.user_name = self.user.user_name()
        self.temp_mode = self.user.temp_mode()

        self.setWindowTitle(Strings.Window.Title + self.user_name +
                            (Strings.Window.TempTitle if self.temp_mode else ""))
        self.setFixedSize(UI.WindowSize)

        # Component declaration
        self.m_btn_user = QPushButton(self)
        self.m_btn_user.setText(Strings.UserMode.BtnTemp if self.temp_mode else Strings.UserMode.BtnUser)
        self.m_btn_user.setGeometry(UI.UserBtnGeo)

        self.m_combo_proj = QComboBox(self)
        self.m_combo_proj.setGeometry(UI.ProjComboGeo)

        self.m_combo_unit = QComboBox(self)
        self.m_combo_unit.setGeometry(UI.UnitComboGeo)

        self.m_btn_sync = QPushButton(Strings.Sync.Btn, self)
        self.m_btn_sync.setGeometry(UI.SyncBtnGeo)

        self.m_btn_upload = QPushButton(Strings.UploadData.Btn, self)
        self.m_btn_upload.setGeometry(UI.UploadDataBtnGeo)

        self.m_btn_history = QPushButton(Strings.History.Btn, self)
        self.m_btn_history.setGeometry(UI.HistoryBtnGeo)
        self.m_btn_history.setEnabled(not self.temp_mode)

        self.m_btn_submit = QPushButton(Strings.Submit.Btn, self)
        self.m_btn_submit.setGeometry(UI.SubmitBtnGeo)

        # Signals and Slots binding
        self.signal_bind()

        self.show()

    def signal_bind(self):
        self.m_btn_user.clicked.connect(self.slot_user_mode_change)
        self.m_btn_history.clicked.connect(self.slot_view_history)

    def slot_user_mode_change(self):
        self.user.trigger_temp()

        # Restart the application
        QCoreApplication.quit()
        status = QProcess.startDetached(sys.executable, sys.argv)
        sys.exit(0 if status[0] else 2)

    def slot_view_history(self):
        HistoryDialog(self, self.user_name)
