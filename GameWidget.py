# cython: language_level=3
# -*- mode: python ; coding: utf-8 -*-

from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QApplication

from GameCore import GameCore
from GamePad import OctDirGamePad
import numpy as np


class GameWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.resize(1500, 500)
        self.setWindowTitle("Game Widget")
        self.game = GameCore((200, 200))
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


    def mousePressEvent(self, a0) -> None:
        if self.gameRect.contains(a0.pos()):
            x = int(a0.pos().x() * (self.game.shape[0] / self.gameRect.width()))
            y = int(a0.pos().y() * (self.game.shape[1] / self.gameRect.height()))
            p = self.game.players['host'].robot.pos + np.array([1,1])
            self.game.directMove('host', p)

            def callback():
                self.render()
                QApplication.processEvents()
            self.game.finishHostFrame(callback)

    def paintEvent(self, a0) -> None:
        pt = QPainter(self)
        pt.drawImage(self.gameRect, self.canvas)
        pt.drawImage(self.userRect, self.userView)
        self.setWindowTitle('{}'.format(self.game.players['host'].getExploreRate()))


def testWidget():
    import sys
    app = QApplication(sys.argv)
    win = GameWidget()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    testWidget()
