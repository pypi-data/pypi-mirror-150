import pyqtgraph as pg

from PyQt5 import QtWidgets


class Tree(pg.TreeWidget, QtWidgets.QTreeWidget):
    def __init__(self, parent=None):
        pg.TreeWidget.__init__(self, parent)
        self.itemClicked.disconnect()

    def display_path_list(self, path_list):
        tree = self
        for path in path_list:
            item = TreeItem([path, path])
            tree.addTopLevelItem(item)


class TreeItem(pg.TreeWidgetItem, QtWidgets.QTreeWidgetItem):
    def __init__(self, *args):
        pg.TreeWidgetItem.__init__(self, *args)

    def get_path_file(self):
        return self.text(1)

    def itemClicked(self, col):
        return self.text(col)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    tree = Tree()
    tree.setColumnCount(2)
    # tree.setHeaderHidden(True)
    tree.show()

    app.exec()
