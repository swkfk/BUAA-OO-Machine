import sys

from PyQt6.QtCore import QSize, QRect, QCoreApplication, QProcess
from PyQt6.QtWidgets import QWidget, QPushButton, QComboBox

from src.ui.RegisterDialog import RegisterDialog
from src.core.settings import LocalAuthentic
from src.strings.MainWidget import Strings


class UI:
    WindowSize = QSize(800, 600)
    UserBtnGeo = QRect(20, 20, 100, 30)
    ProjComboGeo = QRect(140, 20, 100, 30)
    UnitComboGeo = QRect(260, 20, 100, 30)
    SyncBtnGeo = QRect(560, 20, 100, 30)
    UploadDataBtnGeo = QRect(680, 20, 100, 30)


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

        # Signals and Slots binding
        self.signal_bind()

        self.show()

    def signal_bind(self):
        self.m_btn_user.clicked.connect(self.slot_user_mode_change)

    def slot_user_mode_change(self):
        self.user.trigger_temp()

        # Restart the application
        QCoreApplication.quit()
        status = QProcess.startDetached(sys.executable, sys.argv)
        sys.exit(0 if status[0] else 2)
