from PyQt6.QtCore import QSettings


class Globals:

    def __init__(self, scope="-"):
        self.settings = QSettings("BUAA-X15-313", "BUAA-OO-Machine-FrontEnd." + scope)

    def __setitem__(self, key, value):
        self.settings.setValue(key, value)
        self.settings.sync()

    def __getitem__(self, item):
        self.settings.sync()
        return self.settings.value(item)

    def __delitem__(self, key):
        self.settings.remove(key)
        self.settings.sync()

    def __contains__(self, item):
        self.settings.sync()
        return self.settings.contains(item)


# Just for test
if __name__ == "__main__":
    Settings1 = Globals()
    print(Settings1.settings.allKeys())

    Settings1["__test__"] = 42
    print(Settings1.settings.allKeys())

    Settings2 = Globals()
    print(Settings2["__test__"], "__test__" in Settings2)

    del Settings2["__test__"]
    print(Settings2.settings.allKeys())
