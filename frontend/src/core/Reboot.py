from PyQt6.QtCore import QCoreApplication, QProcess

import sys


def reboot():
    QCoreApplication.quit()
    status = QProcess.startDetached(sys.executable, sys.argv)
    sys.exit(0 if status[0] else 2)
