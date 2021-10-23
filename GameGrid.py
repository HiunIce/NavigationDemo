from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QColor

import numpy as np
import cv2
import rrtUtils

class GameGrid:
    def __init__(self, shape=(1000, 1000)):
        self.__baseMap = np.zeros(shape=shape, dtype=np.uint8)
        self.currentMap = np.zeros(shape=shape, dtype=np.uint8)
        self.makeTestGrid()

    def updateGameGrid(self, players):
        self.currentMap = self.__baseMap.copy()
        # for p in players:
        #     self.currentMap[p.robot.pos[0], p.robot.pos[1]] = p.robot.type

    def setBaseMap(self, img):
        if isinstance(img, str):
            img = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2GRAY)
        self.__baseMap = img

    def getCanvas(self):
        return rrtUtils.toQImage(cv2.cvtColor(self.currentMap, cv2.COLOR_GRAY2BGR))

    def makeTestGrid(self):

        self.__baseMap[0:10, :] = 255
        self.__baseMap[self.__baseMap.shape[0]-3:, :] = 255
        self.__baseMap[:, :10] = 255
        self.__baseMap[:, self.__baseMap.shape[1]-3:] = 255
        self.__baseMap[:, 0:4] = 255

        self.__baseMap[50, 60:120] = 255
        self.__baseMap[120, :120] = 255
        cv2.line(self.__baseMap, (100, 200), (100, 300), 255, thickness=1, lineType=4, shift=0)
        cv2.line(self.__baseMap, (200, 200), (200, 300), 255, thickness=1, lineType=4, shift=0)
        cv2.line(self.__baseMap, (150, 0), (150, 100), 255, thickness=1, lineType=4, shift=0)
        cv2.line(self.__baseMap, (200, 0), (200, 100), 255, thickness=1, lineType=4, shift=0)

        self.currentMap = self.__baseMap.copy()