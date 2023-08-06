import os
import sys
import traceback
from logging import Handler

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
from loguru import logger as __logger


def get_a_logger(sink, name):
    __logger.add(sink,
                 filter=lambda record:
                 True if record["extra"].get('name', None) and record["extra"]['name'] == name else False)
    logger = __logger.bind(name=name)
    return logger


class TextHandler(Handler, QObject):
    signal_text = pyqtSignal(str)

    def __init__(self, parent=None, level=0):
        super().__init__(level)
        super(QObject, self).__init__(parent)

        self.error_textbox = QtWidgets.QPlainTextEdit(parent)
        self.error_textbox.setMaximumBlockCount(100)
        self.error_textbox.setReadOnly(True)
        self.error_textbox.setHidden(True)

        self.logger_error = get_a_logger(f'./log/error/log.txt', 'logger_error')
        get_a_logger(self, 'logger_error')

        sys.excepthook = self.__handle_exception

    def __handle_exception(self, exc_type, exc_value, ttraceback):
        # first logger
        error_message = ''.join(traceback.format_exception(exc_type, exc_value, ttraceback))  # 异常信息
        try:
            self.logger_error.error(f"未知程序错误：{error_message}")
        except:
            self.logger_error.error('输出__HandleException信息失败')

    def emit(self, record):
        msg = record.msg
        self.signal_text.emit(msg)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    handel = TextHandler()
    print(handel.asfulj)
