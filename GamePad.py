# cython: language_level=3
# -*- mode: python ; coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton


class CrossButton(QWidget):
    clicked = pyqtSignal(float, float)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.btnsize = [30, 30]
        self.btnup = QPushButton("↑", self)
        self.btndown = QPushButton("↓", self)
        self.btnleft = QPushButton("←", self)
        self.btnright = QPushButton("→", self)
        for btn in [self.btnup, self.btndown, self.btnleft, self.btnright]:
            btn.resize(self.btnsize[0], self.btnsize[1])
        self.btnup.clicked.connect(lambda: self.clicked.emit(0, 1))
        self.btndown.clicked.connect(lambda: self.clicked.emit(180, 1))
        self.btnleft.clicked.connect(lambda: self.clicked.emit(270, 1))
        self.btnright.clicked.connect(lambda: self.clicked.emit(90, 1))

    def getBtnList(self):
        return [self.btnup, self.btndown, self.btnleft, self.btnright]

    def resizeEvent(self, a0):
        sz = self.btnsize
        self.btnup.setGeometry((self.width() - sz[0]) / 2, 0, sz[0], sz[1])
        self.btndown.setGeometry((self.width() - sz[0]) / 2, self.height() - sz[1], sz[0], sz[1])
        self.btnleft.setGeometry(0, (self.height() - sz[1]) / 2, sz[0], sz[1])
        self.btnright.setGeometry(self.width() - sz[0], (self.height() - sz[1]) / 2, sz[0], sz[1])


class OctDirGamePad(CrossButton):
    def __init__(self, parent=None):
        CrossButton.__init__(self, parent=parent)
        self.btnsize = [30, 30]
        self.btn_left_up = QPushButton("↖", self)
        self.btn_left_down = QPushButton("↙", self)
        self.btn_right_up = QPushButton("↗", self)
        self.btn_right_down = QPushButton("↘", self)
        for btn in self.getBtnList():
            btn.resize(self.btnsize[0], self.btnsize[1])
            btn.setAutoRepeat(True)
        self.btn_left_up.clicked.connect(lambda: self.clicked.emit(315, 1))
        self.btn_left_down.clicked.connect(lambda: self.clicked.emit(225, 1))
        self.btn_right_up.clicked.connect(lambda: self.clicked.emit(45, 1))
        self.btn_right_down.clicked.connect(lambda: self.clicked.emit(135, 1))

    def getBtnList(self):
        return [self.btnup, self.btndown, self.btnleft, self.btnright,
                self.btn_left_up, self.btn_left_down, self.btn_right_up, self.btn_right_down]

    def resizeEvent(self, a0):
        sz = self.btnsize
        self.btn_left_up.setGeometry(0, 0, *sz)
        self.btn_left_down.setGeometry(0, self.height()-sz[1], *sz)
        self.btn_right_up.setGeometry(self.width()-sz[0], 0, *sz)
        self.btn_right_down.setGeometry(self.width()-sz[0], self.height()-sz[1], *sz)

        self.btnup.setGeometry((self.width() - sz[0]) / 2, 0, sz[0], sz[1])
        self.btndown.setGeometry((self.width() - sz[0]) / 2, self.height() - sz[1], sz[0], sz[1])
        self.btnleft.setGeometry(0, (self.height() - sz[1]) / 2, sz[0], sz[1])
        self.btnright.setGeometry(self.width() - sz[0], (self.height() - sz[1]) / 2, sz[0], sz[1])