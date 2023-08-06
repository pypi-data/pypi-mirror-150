from pyqtgraph.imageview import ImageView as PgImageView
from pyqtgraph.graphicsItems.ViewBox import ViewBox as PgViewBox
from pyqtgraph.widgets.GraphicsView import GraphicsView as PgGraphicsView
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsView


class ImageViewer(PgImageView, QtWidgets.QWidget):
    def __init__(self, *args):
        PgImageView.__init__(self, *args)

        self.ui.menuBtn.setHidden(True)
        self.ui.roiBtn.setHidden(True)

        self.sig_transform_change = self.view.sigTransformChanged

        # 重载graphicsView类对象
        # 删除原来的graphicsView对象
        # parent = self.ui.graphicsView.parent()
        # self.ui.graphicsView.deleteLater()

        # 生成新的graphicsView对象
        # gpw = GraphicsView(parent, None, 'red')
        # self.ui.graphicsView = gpw
        # self.ui.gridLayout.addWidget(gpw, 0, 0, 2, 1)
        # self.ui.graphicsView.setCentralItem(self.view)
        #
        # self.graphicsView = gpw
        # self.graphicsView.image_item = self.imageItem

    def link_scale_with_another_imw(self, imw):
        self.view.setXLink(imw.view)
        self.view.setYLink(imw.view)


class GraphicsView(PgGraphicsView, QGraphicsView):
    # 缩放联动信号
    sig_scale = QtCore.pyqtSignal(int, int, QtGui.QTransform, int)
    # 移动联动信号
    sig_move = QtCore.pyqtSignal(object, object)

    def __init__(self, *args):
        PgGraphicsView.__init__(self, *args)
        self._zoom = 0

        # 在鼠标处scale,XXX,设置成拖手拖图限制边缘
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def link_scale_with_other_gpv(self, gpv: 'GraphicsView'):
        self.sig_scale.connect(gpv.set_transform)
        self.sig_move.connect(gpv.move_img)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self._zoom += 1
        else:
            factor = 0.8
            self._zoom -= 1
        if self._zoom > 0:
            self.scale(factor, factor)
        elif self._zoom == 0:
            self.fit_in_view()
            pass
        else:
            self._zoom = 0

    def fit_in_view(self):
        rect = self.centralWidget.rect()
        self.fitInView(rect)
        self._zoom = 0

    def mouseMoveEvent(self, ev):
        super(GraphicsView, self).mouseMoveEvent(ev)
        if self.hasFocus():
            self.sig_move.emit(self.horizontalScrollBar().value(),
                               self.verticalScrollBar().value())
