import sys
import traceback as tb

from PyQt6.QtWidgets import QApplication, QMessageBox

from src.ui.MainWidget import MainWidget


def exception_hook(exctype, value, traceback):
    s = "\n".join(tb.format_exception(exctype, value, traceback))
    QMessageBox.critical(None, "Exception detected!", s)
    sys.exit(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.excepthook = exception_hook
    widget = MainWidget()
    sys.exit(app.exec())
