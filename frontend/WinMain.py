import sys
import traceback as tb
from tkinter import messagebox

dependency = ["PyQt6", "QDarkStyle", "requests", "websocket-client（04xxxx 版本增加）"]

def exception_hook(exctype, value, traceback):
    if exctype == ModuleNotFoundError:
        messagebox.showerror("模块未安装！", "请使用 pip 安装下列模块\n" + "\n".join(dependency))
        sys.exit(1)
    s = "\n".join(tb.format_exception(exctype, value, traceback))
    messagebox.showerror("Exception detected!", s)
    sys.exit(1)


sys.excepthook = exception_hook


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    from src.ui.MainWidget import MainWidget

    app = QApplication(sys.argv)
    widget = MainWidget()
    sys.exit(app.exec())
