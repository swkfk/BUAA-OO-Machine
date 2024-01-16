from PyQt6.QtWidgets import QWidget

from src.ui.RegisterDialog import RegisterDialog
from src.core.settings import LocalAuthentic


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()

        self.user = LocalAuthentic.User()
        if self.user.status() == self.user.UserStatus.NONE:
            RegisterDialog(self, self.user.create_user)

        self.user_name = self.user.user_name()
        self.temp_mode = self.user.temp_mode()

        self.show()
