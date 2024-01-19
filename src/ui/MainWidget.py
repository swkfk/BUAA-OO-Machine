import sys

from PyQt6.QtCore import QSize, QRect, QCoreApplication, QProcess, Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QComboBox, QVBoxLayout, QScrollArea, QLineEdit

from src.ui.PointArea import PointArea
from src.ui.RegisterDialog import RegisterDialog
from src.ui.HistoryDialog import HistoryDialog
from src.core.settings import LocalAuthentic
from src.core.settings.ServerConfig import server_config
from src.core.requests.CheckPointList import GetProjList, GetUnitList, GetPointInfo
from src.strings.MainWidget import Strings


class UI:
    WindowSize = QSize(800, 600)

    UserBtnGeo = QRect(20, 20, 100, 30)
    ProjComboGeo = QRect(140, 20, 190, 30)
    UnitComboGeo = QRect(350, 20, 190, 30)
    SyncBtnGeo = QRect(560, 20, 100, 30)
    UploadDataBtnGeo = QRect(680, 20, 100, 30)

    UrlInputGeo = QRect(140, 60, 330, 30)
    PortInputGeo = QRect(480, 60, 60, 30)

    HistoryBtnGeo = QRect(560, 60, 100, 30)
    SubmitBtnGeo = QRect(680, 60, 100, 30)

    ScrollAreaGeo = QRect(20, 110, 760, 460)

    @staticmethod
    def ScrollWidgetSize(c):
        return QSize(740, 80 * c)


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

        self.m_line_url = QLineEdit(server_config["url"], self)
        self.m_line_url.setGeometry(UI.UrlInputGeo)
        self.m_line_url.setPlaceholderText(Strings.Server.HintUrl)

        self.m_line_port = QLineEdit(server_config["port"], self)
        self.m_line_port.setGeometry(UI.PortInputGeo)
        self.m_line_port.setPlaceholderText(Strings.Server.HintPort)

        self.m_widget_list_point = []
        self.m_widget_point = QWidget()
        self.m_layout_point = QVBoxLayout()
        self.m_scroll_point = QScrollArea(self)
        self.m_scroll_point.setGeometry(UI.ScrollAreaGeo)

        # Signals and Slots binding
        self.signal_bind()

        # Update the data shown in the main widget
        self.proj_lst = []
        self.unit_lst = []
        self.point_lst = []
        self.slot_update_proj()

        self.show()

    def signal_bind(self):
        self.m_btn_user.clicked.connect(self.slot_user_mode_change)
        self.m_btn_history.clicked.connect(self.slot_view_history)
        self.m_btn_sync.clicked.connect(self.slot_update_proj)
        self.m_line_url.textChanged.connect(self.slot_url_modify)
        self.m_line_port.textChanged.connect(self.slot_port_modify)
        self.m_combo_proj.currentIndexChanged.connect(self.slot_update_unit)
        self.m_combo_unit.currentIndexChanged.connect(self.slot_update_point)

    def slot_user_mode_change(self):
        self.user.trigger_temp()

        # Restart the application
        QCoreApplication.quit()
        status = QProcess.startDetached(sys.executable, sys.argv)
        sys.exit(0 if status[0] else 2)

    def slot_url_modify(self):
        server_config["url"] = self.m_line_url.text()

    def slot_port_modify(self):
        server_config["port"] = self.m_line_port.text()

    def slot_view_history(self):
        HistoryDialog(self, self.user_name)

    def slot_update_proj(self):
        self.proj_lst = reversed(GetProjList())
        self.m_combo_proj.clear()
        self.m_combo_proj.addItems(self.proj_lst)

    def slot_update_unit(self):
        if self.m_combo_proj.count() == 0:
            return
        self.unit_lst = reversed(GetUnitList(self.m_combo_proj.count() - self.m_combo_proj.currentIndex() - 1))
        self.m_combo_unit.clear()
        self.m_combo_unit.addItems(self.unit_lst)

    def slot_update_point(self):
        if self.m_combo_unit.count() == 0:
            return
        self.point_lst = GetPointInfo(self.user_name if not self.temp_mode else "__TEST__",
                                      self.m_combo_proj.count() - self.m_combo_proj.currentIndex() - 1,
                                      self.m_combo_unit.count() - self.m_combo_unit.currentIndex() - 1)

        self.m_widget_list_point.clear()
        while self.m_layout_point.count() > 0:
            w = self.m_layout_point.takeAt(0).widget()
            self.m_layout_point.removeWidget(w)
            w.deleteLater()

        for idx, point in enumerate(self.point_lst):
            self.m_widget_list_point.append(PointArea(idx, point["same"], point["diff"]))
        for widget in self.m_widget_list_point:
            self.m_layout_point.addWidget(widget)
        self.m_widget_point.resize(UI.ScrollWidgetSize(len(self.m_widget_list_point)))
        self.m_widget_point.setLayout(self.m_layout_point)
        self.m_scroll_point.setWidget(self.m_widget_point)
