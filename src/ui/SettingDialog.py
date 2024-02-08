from PyQt6.QtCore import QSize, QRect, QUrl
from PyQt6.QtWidgets import QDialog, QGridLayout, QGroupBox, QPushButton, QLineEdit, QFileDialog, QMessageBox, \
    QLabel

from src.core.requests.CheckPointList import ConnectTest
from src.core.requests.RequestThread import RequestData
from src.core.settings.ServerConfig import server_config
from src.strings.SettingDialog import Strings
from src.core.settings.FileSystemConfig import FileSystemConfig


class UI:
    WindowSize = QSize(400, 240)
    GroupFsGeo = QRect(10, 10, 380, 100)
    GroupConnGeo = QRect(10, 120, 380, 100)


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

        # ====== Connection Setting ======
        self.m_grid_conn = QGridLayout()
        self.m_grid_conn.setColumnStretch(0, 3)
        self.m_grid_conn.setColumnStretch(1, 9)
        self.m_grid_conn.setColumnStretch(2, 3)

        self.m_btn_info = QPushButton(Strings.ConnectionSetting.InfoBtn, self)
        self.m_grid_conn.addWidget(self.m_btn_info)
        self.m_line_url = QLineEdit(server_config["url"], self)
        self.m_line_url.setPlaceholderText(Strings.ConnectionSetting.UrlHolder)
        self.m_grid_conn.addWidget(self.m_line_url)
        self.m_line_port = QLineEdit(server_config["port"], self)
        self.m_line_port.setPlaceholderText(Strings.ConnectionSetting.PortHolder)
        self.m_grid_conn.addWidget(self.m_line_port)

        self.m_btn_test = QPushButton(Strings.ConnectionSetting.TestBtn, self)
        self.m_grid_conn.addWidget(self.m_btn_test)
        self.m_label_test = QLabel(self)
        self.m_grid_conn.addWidget(self.m_label_test, 1, 1, 1, 2)

        self.m_group_conn = QGroupBox(Strings.ConnectionSetting.Title, self)
        self.m_group_conn.setGeometry(UI.GroupConnGeo)
        self.m_group_conn.setLayout(self.m_grid_conn)

        # ====== Bind ======
        self.m_btn_storage.clicked.connect(self.slot_get_storage)
        self.m_btn_src.clicked.connect(self.slot_get_src)
        self.m_btn_info.clicked.connect(self.slot_info_clicked)
        self.m_line_url.textChanged.connect(self.slot_url_modify)
        self.m_line_port.textChanged.connect(self.slot_port_modify)
        self.m_btn_test.clicked.connect(self.slot_conn_test)

        # ====== Launch ======
        self.update_status()
        self.exec()

    def slot_get_storage(self):
        self.config.set_storage_path(self.get_path())
        self.update_status()

    def slot_get_src(self):
        self.config.set_src_path(self.get_path())
        self.update_status()

    def slot_info_clicked(self):
        self.m_line_url.setFocus()

    def slot_url_modify(self):
        server_config["url"] = self.m_line_url.text()

    def slot_port_modify(self):
        server_config["port"] = self.m_line_port.text()

    def slot_conn_test(self):
        def aux(response: RequestData):
            if response.status_code == 200:
                hint = response.data
            elif response.status_code == 0:
                hint = "Timeout!"
            else:
                hint = response.data
            self.m_label_test.setText(Strings.ConnectionSetting.Label.format(response.status_code, hint))

        self.m_label_test.setText(Strings.ConnectionSetting.Testing)
        ConnectTest(aux)

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
