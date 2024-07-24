import re
from functools import partial

from PyQt6.QtCore import QSize, QRect, QUrl, pyqtSignal
from PyQt6.QtWidgets import QDialog, QGridLayout, QGroupBox, QPushButton, QLineEdit, QFileDialog, QMessageBox, \
    QLabel, QRadioButton, QWidget, QVBoxLayout, QCheckBox

from src.core.Reboot import reboot
from src.core.requests.SimpleQueryRequests import ConnectTest
from src.core.settings.I18nConfig import set_lang, get_lang
from src.core.settings.JavaConfig import set_main_class, get_main_class, get_ask_each, set_ask_each
from src.core.settings.ServerConfig import server_config, get_ws_addr
from src.core.settings.SystemConfig import is_dark_theme, set_theme, DARK_THEME, LIGHT_THEME
from src.i18n import SettingDialog as Strings, lang_list
from src.core.settings.FileSystemConfig import FileSystemConfig


class UI:
    WindowSize = QSize(650, 500)
    WholeGeo = QRect(10, 10, 630, 480)


class SettingDialog(QDialog):
    sig_theme_change = pyqtSignal()

    def __init__(self, parent, user_name):
        super().__init__(parent)

        self.config = FileSystemConfig()
        self.user = user_name

        self.setWindowTitle(Strings.Window.Title)
        self.resize(UI.WindowSize)

        self.m_layout = QVBoxLayout(self)
        self.m_layout.setGeometry(UI.WholeGeo)

        # ====== File System Setting ======
        self.m_grid_fs = QGridLayout()
        self.m_grid_fs.setColumnStretch(0, 2)
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

        self.m_btn_passwd = QPushButton(Strings.FileSystemSetting.Passwd, self)
        self.m_grid_fs.addWidget(self.m_btn_passwd)
        self.m_line_passwd = QLineEdit(self)
        self.m_line_passwd.setPlaceholderText(Strings.FileSystemSetting.PasswdHint)
        self.m_grid_fs.addWidget(self.m_line_passwd)

        self.m_group_fs = QGroupBox(Strings.FileSystemSetting.Title, self)
        self.m_group_fs.setLayout(self.m_grid_fs)
        self.m_layout.addWidget(self.m_group_fs)

        # ====== Java Setting ======
        self.m_grid_java = QGridLayout()
        self.m_grid_java.setColumnStretch(0, 2)
        self.m_grid_java.setColumnStretch(1, 9)

        self.m_btn_java_class = QPushButton(Strings.JavaSetting.MainClass, self)
        self.m_grid_java.addWidget(self.m_btn_java_class)

        self.m_line_java_class = QLineEdit(get_main_class(), self)
        self.m_line_java_class.setPlaceholderText(Strings.JavaSetting.MainClassHint)
        self.m_line_java_class.setDisabled(get_ask_each())
        self.m_grid_java.addWidget(self.m_line_java_class)
        self.m_line_java_class.textChanged.connect(set_main_class)

        self.m_check_ask = QCheckBox(Strings.JavaSetting.AskEach, self)
        self.m_check_ask.setChecked(get_ask_each())
        self.m_check_ask.toggled.connect(self.slot_java_ask_each)
        self.m_grid_java.addWidget(self.m_check_ask)

        self.m_group_java = QGroupBox(Strings.JavaSetting.Title, self)
        self.m_group_java.setLayout(self.m_grid_java)
        self.m_layout.addWidget(self.m_group_java)

        # ====== Connection Setting ======
        self.m_grid_conn = QGridLayout()
        self.m_grid_conn.setColumnStretch(0, 2)
        self.m_grid_conn.setColumnStretch(1, 6)
        self.m_grid_conn.setColumnStretch(2, 3)

        self.m_btn_info = QPushButton(Strings.ConnectionSetting.InfoBtn, self)
        self.m_grid_conn.addWidget(self.m_btn_info)
        self.m_line_url = QLineEdit(server_config["url"], self)
        self.m_line_url.setPlaceholderText(Strings.ConnectionSetting.UrlHolder)
        self.m_grid_conn.addWidget(self.m_line_url)
        self.m_line_port = QLineEdit(server_config["port"], self)
        self.m_line_port.setPlaceholderText(Strings.ConnectionSetting.PortHolder)
        self.m_grid_conn.addWidget(self.m_line_port)

        self.m_btn_ws = QPushButton(Strings.ConnectionSetting.WsBtn, self)
        self.m_grid_conn.addWidget(self.m_btn_ws)
        self.m_line_ws = QLineEdit(self)
        self.m_line_ws.setReadOnly(True)
        self.m_grid_conn.addWidget(self.m_line_ws, 1, 1, 1, 2)

        self.m_btn_test = QPushButton(Strings.ConnectionSetting.TestBtn, self)
        self.m_grid_conn.addWidget(self.m_btn_test)
        self.m_label_test = QLabel(self)
        self.m_grid_conn.addWidget(self.m_label_test, 2, 1, 1, 2)

        self.m_group_conn = QGroupBox(Strings.ConnectionSetting.Title, self)
        self.m_group_conn.setLayout(self.m_grid_conn)
        self.m_layout.addWidget(self.m_group_conn)

        # ====== System ======
        self.m_grid_sys = QGridLayout()
        self.m_grid_sys.setColumnStretch(0, 4)
        self.m_grid_sys.setColumnStretch(1, 3)
        self.m_grid_sys.setColumnStretch(2, 3)
        self.m_grid_sys.setColumnStretch(3, 12)

        self.m_btn_theme = QPushButton(Strings.SystemConfig.ThemeBtn, self)
        self.m_grid_sys.addWidget(self.m_btn_theme)

        self.m_radio_dark = QRadioButton(Strings.SystemConfig.ThemeDark, self)
        self.m_radio_dark.setChecked(is_dark_theme())
        self.m_radio_dark.toggled.connect(self.slot_set_dark)
        self.m_grid_sys.addWidget(self.m_radio_dark)

        self.m_radio_light = QRadioButton(Strings.SystemConfig.ThemeLight, self)
        self.m_radio_light.setChecked(not is_dark_theme())
        self.m_grid_sys.addWidget(self.m_radio_light)

        self.m_grid_sys.addWidget(QWidget())

        self.m_btn_lang = QPushButton(Strings.SystemConfig.LangBtn, self)
        self.m_grid_sys.addWidget(self.m_btn_lang)

        self.m_btn_langs = []
        for i, (code, text) in enumerate(lang_list):
            btn = QPushButton(text, self)
            btn.setEnabled(code != get_lang())
            btn.clicked.connect(partial(self.slot_change_lang, code))
            self.m_btn_langs.append(btn)
            self.m_grid_sys.addWidget(btn)

        self.m_group_sys = QGroupBox(Strings.SystemConfig.Title, self)
        self.m_group_sys.setLayout(self.m_grid_sys)
        self.m_layout.addWidget(self.m_group_sys)

        # ====== Bind ======
        self.m_btn_storage.clicked.connect(self.slot_get_storage)
        self.m_btn_src.clicked.connect(self.slot_get_src)
        self.m_btn_info.clicked.connect(self.slot_info_clicked)
        self.m_line_url.textChanged.connect(self.slot_url_modify)
        self.m_line_url.textChanged.connect(self.slot_addr_changed)
        self.m_line_port.textChanged.connect(self.slot_port_modify)
        self.m_line_port.textChanged.connect(self.slot_addr_changed)
        self.m_line_passwd.textChanged.connect(self.config.set_zip_passwd)
        self.m_btn_test.clicked.connect(self.slot_conn_test)

        # ====== Launch ======
        self.update_status()
        # self.exec()

    @staticmethod
    def slot_change_lang(lang):
        if lang == get_lang():
            return
        set_lang(lang)
        reboot()

    def slot_addr_changed(self):
        host = self.m_line_url.text()
        port = self.m_line_port.text()
        self.m_line_ws.setText(get_ws_addr(host, port))

    def slot_get_storage(self):
        self.config.set_storage_path(self.get_path())
        self.update_status()

    def slot_get_src(self):
        self.config.set_src_path(self.get_path())
        self.update_status()

    def slot_java_ask_each(self):
        self.m_line_java_class.setDisabled(self.m_check_ask.isChecked())
        set_ask_each(self.m_check_ask.isChecked())

    def slot_info_clicked(self):
        self.m_line_url.setFocus()

    def slot_url_modify(self):
        server_config["url"] = self.m_line_url.text()

    def slot_port_modify(self):
        server_config["port"] = self.m_line_port.text()

    def slot_conn_test(self):
        def aux(s, replace=False):
            if replace:
                self.m_label_test.setText(s)
            else:
                self.m_label_test.setText(self.m_label_test.text() + s)
        ConnectTest(aux, self.user)

    def get_path(self):
        path = QFileDialog.getExistingDirectoryUrl(self, "", QUrl("./")).toLocalFile()
        if path != "" and not FileSystemConfig.check_access(path):
            QMessageBox.critical(self, "Invalid Path!", "Non-exist or No Permission")
            path = ""
        return path

    def slot_set_dark(self, b):
        set_theme(DARK_THEME if b else LIGHT_THEME)
        self.sig_theme_change.emit()

    def update_status(self):
        s = self.config.get_storage_path()
        self.m_line_storage.setText(s if s else Strings.Common.Unknown)
        s = self.config.get_src_path()
        self.m_line_src.setText(s if s else Strings.Common.Unknown)
        self.m_line_passwd.setText(self.config.get_zip_passwd())
        self.slot_addr_changed()
