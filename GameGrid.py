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
        for p in players:
            self.currentMap[p.robot.pos[0], p.robot.pos[1]] = p.robot.type

    def setBaseMap(self, img):
        if isinstance(img, str):
            img = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2GRAY)
        self.__baseMap = img

    def getCanvas(self):
        return rrtUtils.toQImage(cv2.cvtColor(self.currentMap, cv2.COLOR_GRAY2BGR))

    def makeTestGrid(self):
        seeds = [1,2,3,4,5,6,7,8,9,10]
        np.random.seed(10) #15
        for i in range(10):
            p1 = np.random.randint(0, self.__baseMap.shape[0], 2)
            p2 = np.copy(p1)
            p2[np.random.randint(0, 2)] = np.random.randint(0, 100)
            cv2.line(self.__baseMap, p1, p2, 255, thickness=3, lineType=4, shift=0)

        self.currentMap = self.__baseMap.copy()