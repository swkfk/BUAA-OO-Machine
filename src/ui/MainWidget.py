import sys

from PyQt6.QtCore import QSize, QRect, QCoreApplication, QProcess
from PyQt6.QtWidgets import QWidget, QPushButton, QComboBox, QVBoxLayout, QScrollArea, QMainWindow, QMessageBox, \
    QGridLayout

from src.core.requests.RequestThread import RequestData
from src.ui.PointArea import PointArea
from src.ui.RegisterDialog import RegisterDialog
from src.ui.HistoryDialog import HistoryDialog
from src.core.settings import LocalAuthentic
from src.core.requests.CheckPointList import GetProjList, GetUnitList, GetPointInfo
from src.strings.MainWidget import Strings
from src.ui.SettingDialog import SettingDialog
from src.ui.SubmitDialog import SubmitDialog


class UI:
    WindowSize = QSize(590, 500)

    BtnWidgetGeo = QRect(10, 0, 570, 90)

    ScrollAreaGeo = QRect(20, 90, 550, 380)

    @staticmethod
    def ScrollWidgetSize(c):
        return QSize(530, 80 * c)


class MainWidget(QMainWindow):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.user = LocalAuthentic.User()
        if self.user.status() == self.user.UserStatus.NONE:
            RegisterDialog(self, self.user.create_user)
            SettingDialog(self)

        self.user_name = self.user.user_name()
        self.temp_mode = self.user.temp_mode()

        self.setWindowTitle(Strings.Window.Title + self.user_name +
                            (Strings.Window.TempTitle if self.temp_mode else ""))
        self.setFixedSize(UI.WindowSize)

        # Component declaration
        self.m_widget_btn = QWidget(self)
        self.m_widget_btn.setGeometry(UI.BtnWidgetGeo)

        self.m_grid_btn = QGridLayout()
        for c, s in [(0, 1), (1, 2), (2, 1), (3, 1)]:
            self.m_grid_btn.setColumnStretch(c, s)

        self.m_btn_user = QPushButton(self)
        self.m_btn_user.setText(Strings.UserMode.BtnTemp if self.temp_mode else Strings.UserMode.BtnUser)
        self.m_grid_btn.addWidget(self.m_btn_user)

        self.m_combo_proj = QComboBox(self)
        self.m_grid_btn.addWidget(self.m_combo_proj)

        self.m_btn_sync = QPushButton(Strings.Sync.Btn, self)
        self.m_grid_btn.addWidget(self.m_btn_sync)

        self.m_btn_upload = QPushButton(Strings.UploadData.Btn, self)
        self.m_grid_btn.addWidget(self.m_btn_upload)

        self.m_btn_setting = QPushButton(Strings.Setting.Btn, self)
        self.m_grid_btn.addWidget(self.m_btn_setting)

        self.m_combo_unit = QComboBox(self)
        self.m_grid_btn.addWidget(self.m_combo_unit)

        self.m_btn_history = QPushButton(Strings.History.Btn, self)
        self.m_grid_btn.addWidget(self.m_btn_history)
        self.m_btn_history.setEnabled(not self.temp_mode)

        self.m_btn_submit = QPushButton(Strings.Submit.Btn, self)
        self.m_grid_btn.addWidget(self.m_btn_submit)

        self.m_widget_btn.setLayout(self.m_grid_btn)

        self.m_widget_list_point = []
        self.m_widget_point = QWidget()
        self.m_layout_point = QVBoxLayout()
        self.m_scroll_point = QScrollArea(self)
        self.m_scroll_point.setGeometry(UI.ScrollAreaGeo)

        self.status_ready()

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
        self.m_btn_setting.clicked.connect(self.slot_open_setting)
        self.m_btn_sync.clicked.connect(self.slot_update_proj)
        self.m_combo_proj.currentIndexChanged.connect(self.slot_update_unit)
        self.m_combo_unit.currentIndexChanged.connect(self.slot_update_point)
        self.m_btn_submit.clicked.connect(self.slot_submit)

    def real_user(self):
        return self.user_name if not self.temp_mode else "__TEST__"

    def proj_id(self):
        return self.m_combo_proj.count() - self.m_combo_proj.currentIndex() - 1

    def unit_id(self):
        return self.m_combo_unit.count() - self.m_combo_unit.currentIndex() - 1

    def slot_user_mode_change(self):
        self.user.trigger_temp()

        # Restart the application
        QCoreApplication.quit()
        status = QProcess.startDetached(sys.executable, sys.argv)
        sys.exit(0 if status[0] else 2)

    def slot_view_history(self):
        HistoryDialog(self, self.user_name)

    def slot_open_setting(self):
        SettingDialog(self)

    def slot_update_proj(self):
        def aux(response: RequestData):
            self.status_ready()
            if response.status_code == 200:
                self.proj_lst = reversed(response.data)
            elif response.status_code == 0:
                self.proj_lst = []
                QMessageBox.critical(self, "[Projects] Connect Timeout!", response.data["."])
            else:
                self.proj_lst = []
                QMessageBox.critical(self, "[Projects] Unhandled Error!", response.data["."])
            self.m_combo_proj.clear()
            self.m_combo_proj.addItems(self.proj_lst)

        self.status_busy(Strings.Status.BusyUpdateProject)
        GetProjList(aux)

    def slot_update_unit(self):
        def aux(response: RequestData):
            self.status_ready()
            if response.status_code == 200:
                self.unit_lst = reversed(response.data)
            else:
                self.unit_lst = []
                QMessageBox.critical(self, "[Units] Unhandled Error!", response.data["."])
            self.m_combo_unit.clear()
            self.m_combo_unit.addItems(self.unit_lst)

        if self.m_combo_proj.count() == 0:
            return
        self.status_busy(Strings.Status.BusyUpdateUnit)
        GetUnitList(aux, self.proj_id())

    def slot_update_point(self):
        def aux(response: RequestData):
            self.status_ready()
            if response.status_code == 200:
                self.point_lst = reversed(response.data)
            else:
                self.point_lst = []
                QMessageBox.critical(self, "[Points] Unhandled Error!", response.data["."])

            self.m_widget_list_point.clear()
            while self.m_layout_point.count() > 0:
                w = self.m_layout_point.takeAt(0).widget()
                self.m_layout_point.removeWidget(w)
                w.deleteLater()

            for idx, point in enumerate(self.point_lst):
                pa = PointArea(
                    idx, point["same"], point["diff"],
                    self.real_user(), self.proj_id(), self.unit_id(),
                    (self.status_ready, self.status_busy)
                )
                self.m_widget_list_point.append(pa)
                self.m_layout_point.addWidget(pa)
            self.m_widget_point.resize(UI.ScrollWidgetSize(len(self.m_widget_list_point)))
            self.m_widget_point.setLayout(self.m_layout_point)
            self.m_scroll_point.setWidget(self.m_widget_point)

        if self.m_combo_unit.count() == 0:
            return
        self.status_busy(Strings.Status.BusyUpdatePoint)
        GetPointInfo(aux, self.real_user(), self.proj_id(), self.unit_id())

    def slot_submit(self):
        SubmitDialog(self, self.real_user(), self.proj_id(), self.unit_id())

    def status_ready(self):
        self.statusBar().showMessage(Strings.Status.Ready, 0)

    def status_busy(self, s: str):
        self.statusBar().showMessage(s, 0)
