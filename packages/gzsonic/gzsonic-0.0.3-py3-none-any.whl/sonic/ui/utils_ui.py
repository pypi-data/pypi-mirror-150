from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import QtWidgets
import datetime

today = datetime.date.today()


def init_app():
    return QtWidgets.QApplication([])


class SonicSignal(QObject):
    signal_str = pyqtSignal(str)
    signal_int = pyqtSignal(int)
    signal_float = pyqtSignal(float)
    signal_dict = pyqtSignal(dict)
    signal_func = pyqtSignal(dict)
