# coding: utf-8
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt, QFile, QTextCodec
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QWidget
import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import history
import viewconfig


class kdcomicbookviewer(QWidget):
    def __init__(self):
        super(kdcomicbookviewer, self).__init__()
        loadUi("kdcomicbookviewer.ui", self)
        self.img_index = None
        self.view_mode = "scaledToWidth"
        self.fullscreen_mode = False
        self.img = QImage()
        jContent = history.get_history()
        if jContent is not None:
            self.filePath = jContent["img_path"]
            self.img_index = jContent["img_index"]
            self.getFilesFormDir()
            self.loadImage(self.img_index)
        print(dir(self.toolbar))
        # ~ 加载阅读模式
        viewconf = viewconfig.get_viewconfig()
        if viewconf is not None:
            self.view_mode = viewconf["view_mode"]
        self.toolbarLayout.setAlignment(Qt.AlignRight)

    @pyqtSlot()
    def on_pb_open_file_clicked(self):
        self.filePath = QFileDialog.getExistingDirectory(None, "open", r"/tmp/a.jpg")
        self.getFilesFormDir()
        self.loadImage(0)
        self.img_index = 0
        history.set_history(self.filePath, self.img_index)

    @pyqtSlot()
    def on_comicViewer_resize(self):
        print("resize")

    def getFilesFormDir(self):
        dirs = QDir(self.filePath)
        dirs.setNameFilters(["*.jpg", "*.png", "*.PNG"])
        self.files = dirs.entryList()
        print(self.files)

    def resizeEvent(self, event):
        print("resizeEvent", self.graphicsView.width())
        if self.hasattr("img_index"):
            self.loadImage(self.img_index)

    def loadImage(self, image_index):
        # ~ if self.img.isNull() == False :
        print("第" + str(image_index) + "张图片")
        if image_index >= len(self.files):
            image_index = 0
        print(self.filePath + "/" + self.files[image_index])
        self.img.load(self.filePath + "/" + self.files[image_index])
        if self.view_mode == "scaledToWidth":
            self.img = self.img.scaledToWidth(self.graphicsView.width())
        elif self.view_mode == "scaledToHeight":
            self.img = self.img.scaledToHeight(self.graphicsView.heigth())
        scene = QGraphicsScene()
        map1 = QPixmap()
        map1.load(self.filePath + "/" + self.files[image_index])
        self.img = map1
        scene.addPixmap(map1)
        self.graphicsView.setScene(scene)
        self.img_index = image_index

        status_text = (
            str(image_index + 1)
            + "页/"
            + str(len(self.files))
            + ","
            + str(map1.width())
            + "x"
            + str(map1.height())
            + ","
            + self.files[image_index]
        )
        self.statusbar.setText(status_text)

    def keyPressEvent(self, event):
        # 这里event.key（）显示的是按键的编码
        curKey = event.key()
        print("按下：" + str(event.key()))
        # 举例，这里Qt.Key_A注意虽然字母大写，但按键事件对大小写不敏感
        if curKey == Qt.Key_N or curKey == Qt.Key_Space or curKey == Qt.Key_B:
            self.loadImage(self.img_index + 1)
            history.set_history(self.filePath, self.img_index - 1)
        elif curKey == Qt.Key_P or curKey == Qt.Key_F:
            self.loadImage(self.img_index - 1)
            history.set_history(self.filePath, self.img_index - 1)
        elif curKey == Qt.Key_Equal:
            self.graphicsView.scale(1.1, 1.1)
        elif str(curKey) == "45":
            self.graphicsView.scale(0.9, 0.9)
        elif curKey == Qt.Key_F11:
            self.on_pb_fullscreen_clicked()
        elif curKey == Qt.Key_Escape:
            self.showNormal()
            self.toolbar.show()
            self.fullscreen_mode = False

    @pyqtSlot()
    def on_pb_larger_clicked(self):
        self.graphicsView.scale(1.1, 1.1)

    @pyqtSlot()
    def on_pb_smaller_clicked(self):
        self.graphicsView.scale(0.9, 0.9)

    @pyqtSlot()
    def on_pb_fit_height_clicked(self):
        heigth_ratio = self.graphicsView.height() / self.img.height()
        self.graphicsView.resetTransform()
        self.graphicsView.scale(heigth_ratio, heigth_ratio)

    @pyqtSlot()
    def on_pb_fit_width_clicked(self):
        width_ratio = self.graphicsView.width() / self.img.width()
        self.graphicsView.resetTransform()
        self.graphicsView.scale(width_ratio, width_ratio)

    @pyqtSlot()
    def on_pb_fit_window_clicked(self):
        width_ratio = self.graphicsView.width() / self.img.width()
        height_ratio = self.graphicsView.height() / self.img.height()
        print("width_ratio", width_ratio, "height_ratio", height_ratio)
        self.graphicsView.resetTransform()
        if width_ratio < height_ratio:
            self.graphicsView.scale(width_ratio, width_ratio)
        else:
            self.graphicsView.scale(height_ratio, height_ratio)

    @pyqtSlot()
    def on_pb_fullscreen_clicked(self):
        if self.fullscreen_mode:
            self.showNormal()
            self.fullscreen_mode = False
            self.toolbar.show()
        else:
            self.showFullScreen()
            self.fullscreen_mode = True
            self.toolbar.hide()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = kdcomicbookviewer()
    win.show()
    if "2" == "2":
        print("2")
    sys.exit(app.exec_())
