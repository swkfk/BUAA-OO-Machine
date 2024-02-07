from PyQt6.QtCore import QSize, QRect, QUrl
from PyQt6.QtWidgets import QDialog, QGridLayout, QGroupBox, QPushButton, QLineEdit, QFileDialog, QMessageBox

from src.strings.SettingDialog import Strings
from src.core.settings.FileSystemConfig import FileSystemConfig


class UI:
    WindowSize = QSize(400, 200)
    GroupFsGeo = QRect(10, 10, 380, 100)


class SettingDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.config = FileSystemConfig()

        self.setWindowTitle(Strings.Window.Title)
        self.resize(UI.WindowSize)

        # ====== File System Setting ======
        self.m_grid_fs = QGridLayout()
        self.m_grid_fs.setColumnStretch(0, 3)
        self.m_grid_fs.setColumnStretch(1, 9)

        self.m_btn_storage = QPushButton(Strings.FileSystemSetting.Storage, self)
        self.m_grid_fs.addWidget(self.m_btn_storage)
        self.m_line_storage = QLineEdit(self)
        self.m_line_storage.setReadOnly(True)
        self.m_grid_fs.addWidget(self.m_line_storage)

        self.m_btn_src = QPushButton(Strings.FileSystemSetting.Src, self)
        self.m_grid_fs.addWidget(self.m_btn_src)
        self.m_line_src = QLineEdit(self)
        self.m_line_src.setReadOnly(True)
        self.m_grid_fs.addWidget(self.m_line_src)

        self.m_group_fs = QGroupBox(Strings.FileSystemSetting.Title, self)
        self.m_group_fs.setGeometry(UI.GroupFsGeo)
        self.m_group_fs.setLayout(self.m_grid_fs)

        # ====== Bind ======
        self.m_btn_storage.clicked.connect(self.slot_get_storage)
        self.m_btn_src.clicked.connect(self.slot_get_src)

        # ====== Launch ======
        self.update_status()
        self.exec()

    def slot_get_storage(self):
        self.config.set_storage_path(self.get_path())
        self.update_status()

    def slot_get_src(self):
        self.config.set_src_path(self.get_path())
        self.update_status()

    def get_path(self):
        path = QFileDialog.getExistingDirectoryUrl(self, "", QUrl("./")).toLocalFile()
        if path != "" and not FileSystemConfig.check_access(path):
            QMessageBox.critical(self, "Invalid Path!", "Non-exist or No Permission")
            path = ""
        return path

    def update_status(self):
        s = self.config.get_storage_path()
        self.m_line_storage.setText(s if s else Strings.Common.Unknown)
        s = self.config.get_src_path()
        self.m_line_src.setText(s if s else Strings.Common.Unknown)
