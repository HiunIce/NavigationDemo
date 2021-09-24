# cython: language_level=3
# -*- mode: python ; coding: utf-8 -*-

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtWidgets import QWidget, QApplication, QTextEdit

from GameCore import GameCore
from GamePad import OctDirGamePad
import numpy as np

import RRTBase

class GameWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.resize(1500, 500)
        self.setWindowTitle("Game Widget")
        self.game = GameCore((500,500))
        self.gamePad = OctDirGamePad(self)
        self.gamePad.clicked.connect(self.userInput)
        self.canvas = None
        self.userView = None
        self.gameRect = QRect(0, 0, 1000, 1000)
        self.userRect = QRect(0, 0, 1000, 1000)
        self.render()

    def userInput(self, deg, l):
        scale = int(3)
        dir = np.array([np.sin(np.deg2rad(deg)), np.cos(np.deg2rad(deg))])
        dir[dir < -0.001] = -1
        dir[dir > 0.001] = 1
        dir[1] = -dir[1]
        dir = (dir*l).astype(np.int32) * scale
        self.game.setHostInput(dir)
        self.game.nextFrame()
        self.render()

    def render(self):
        self.canvas = self.game.getCanvas()
        self.userView = self.game.getHostView()
        self.update()

    def resizeEvent(self, a0) -> None:
        spacing = 10
        self.gameRect = QRect(0, 0, self.height(), self.height())
        self.userRect = QRect(self.gameRect.x() + self.gameRect.width() + spacing,
                              0, self.gameRect.width(), self.gameRect.height())
        self.gamePad.setGeometry(self.userRect.x() + self.userRect.width() + spacing,
                                 0, 200, 200)

    def paintEvent(self, a0) -> None:
        pt = QPainter(self)
        pt.drawImage(self.gameRect, self.canvas)
        pt.drawImage(self.userRect, self.userView)

def testWidget():
    import sys
    app = QApplication(sys.argv)
    win = GameWidget()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    testWidget()
