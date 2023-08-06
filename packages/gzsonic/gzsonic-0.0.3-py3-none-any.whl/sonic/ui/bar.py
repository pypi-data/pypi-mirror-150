from PyQt5 import QtWidgets, QtCore


class Bar(QtWidgets.QProgressBar):
    signal_update_bar = QtCore.pyqtSignal(int)
    signal_finish = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(Bar, self).__init__(parent=parent)
        self.setValue(0)

        self.signal_update_bar.connect(self.update_bar)

    def update_bar(self, val):
        self.setValue(val)

    def tqdm(self, iterable, total=None):
        if total is None and iterable is not None:
            try:
                total = len(iterable)
            except (TypeError, AttributeError):
                total = float("inf")
        count = 0
        for i in iterable:
            count += 1
            self.signal_update_bar.emit(int(count / total * 100))
            yield i
        self.signal_finish.emit(self)
        self.signal_update_bar.emit(100)


if __name__ == '__main__':
    from sonic.ui.utils_ui import init_app
    import time, threading

    app = init_app()
    win = Bar()
    win.show()


    def test_tqdm():
        for i in win.tqdm(['aasudl', 'zuixc', r'C:\Users\Administrator\Documents\GitHub\detection\test']):
            print(i)
            time.sleep(0.3)


    # thrad = threading.Thread(target=download_file, args=(url,))
    thrad = threading.Thread(target=test_tqdm)
    thrad.setDaemon(True)
    thrad.start()

    app.exec()
