import threading
import time

from PyQt5 import QtWidgets
from sonic.log import get_a_logger, TextHandler
from sonic.ui.bar import Bar


class TextBox(QtWidgets.QPlainTextEdit):
    def __init__(self, *args, **kwargs):
        super(TextBox, self).__init__(*args, **kwargs)
        self.setReadOnly(True)
        self.setMaximumBlockCount(300)

        self.bar = Bar(self)

        self.handler = TextHandler()
        self.handler.signal_text.connect(self.update_textbox)

        self.logger = get_a_logger(self.handler, f'text_box{id(self)}')

    def update_textbox(self, text):
        textbox = self
        if 'WARNING' in text:
            textbox.appendHtml(f"<pre><font color = #FF7F7F>{text}</font></pre>")
        elif 'ERROR' in text:
            textbox.appendHtml(f"<pre><font color = red>{text}</font></pre>")
        else:
            textbox.appendHtml(f"<pre><font color = black>{text}</font></pre>")

    def tqdm(self, *args, **kwargs):
        return self.bar.tqdm(*args, **kwargs)


if __name__ == '__main__':
    from sonic.ui.utils_ui import init_app

    app = init_app()
    win = TextBox()
    win.show()

    layout = QtWidgets.QVBoxLayout(win)
    layout.addWidget(win)
    layout.addWidget(win.bar)
    logger = win.logger
    logger.info('来自于handler的信号')


    def test_tqdm():
        for i in win.tqdm(['aasudl', 'zuixc', r'C:\Users\Administrator\Documents\GitHub\detection\test']):
            print(i)
            time.sleep(0.3)


    # thrad = threading.Thread(target=download_file, args=(url,))
    thrad = threading.Thread(target=test_tqdm)
    thrad.setDaemon(True)
    thrad.start()

    app.exec()
