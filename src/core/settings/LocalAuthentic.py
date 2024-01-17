from enum import Enum

from src.core.settings import GlobalSettings


class User:
    class UserStatus(Enum):
        NONE = 0  # There are no recordings in the storage
        TEMP = 1  # Temp User Mode, use the common name "__TEST__"
        USER = 2

    def __init__(self):
        self.user_setting = GlobalSettings.Globals("user")

    def status(self):
        if "UserName" not in self.user_setting or "TempMode" not in self.user_setting:
            return self.UserStatus.NONE
        if self.temp_mode():
            return self.UserStatus.TEMP
        else:
            return self.UserStatus.USER

    def user_name(self):
        return self.user_setting["UserName"]

    def temp_mode(self):
        return str(self.user_setting["TempMode"]).lower() == "true"

    def trigger_temp(self):
        self.user_setting["TempMode"] = not self.temp_mode()

    def create_user(self, name):
        self.user_setting["TempMode"] = False
        self.user_setting["UserName"] = name


# Just for test
if __name__ == "__main__":
    user = User()
    print(user.status())

    user.create_user("李华")  # Chinese character tests
    print(user.status(), user.user_name(), user.user_setting["TempMode"])
    print(type(user.user_setting["TempMode"]))

    user.trigger_temp()
    print(user.status(), user.user_name(), user.user_setting["TempMode"])

    user.trigger_temp()
    print(user.status(), user.user_name(), user.user_setting["TempMode"])

    user.user_setting.settings.clear()
    print(user.status())
