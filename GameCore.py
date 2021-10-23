
from GameGrid import GameGrid
from Player import Player
from PyQt5.QtGui import QPainter, QColor
import rrtUtils
import numpy as np

class GameCore:
    def __init__(self, shape=(1000, 1000)):
        self.shape = shape
        self.grid = GameGrid(shape)
        self.players = dict()
        self.playersPrePos = dict()
        self.addPlayer('host', pos=[150, 150])

    def nextFrame(self):
        self.grid.updateGameGrid(self.players.values())
        for k in self.players.keys():
            self.players[k].act(self.grid.currentMap)
            pos = self.players[k].robot.pos
            pre_pos = self.playersPrePos[k]
            diff = [abs(pre_pos[0]-pos[0]), abs(pre_pos[1]-pre_pos[1])]
            if (diff[0] > 1.001) or (diff[1]>1.001):
                print('user', k, 'is cheating', diff)
            self.playersPrePos[k] = pos
            
        
    def finishHostFrame(self, callback):
        while not self.players['host'].decisionList.empty():
            self.nextFrame()
            callback()
        #     self.players['host'].planTheory()
        # # while len(self.players['host'].fronts) != 0:
        # #     self.players['host'].planTheory(self.grid.currentMap)
        while self.players['host'].explore_rate < 0.8:
            self.players['host'].planTheory()
            self.nextFrame()
            callback()


    def setHostInput(self, action):
        self.players['host'].decisionList.put(action)

    def directMove(self, user, pos):
        if self.grid.currentMap[pos[1], pos[0]] == 255:
            print('you clicked the wall')
            return
        self.players[user].clearDecision()
        self.players[user].moveTheory_cheat(self.grid.currentMap, pos)

    def getHostView(self):
        return self.players['host'].getPlayerView()

    def addPlayer(self, name, pos):
        self.players[name] = Player(name, len(self.players) + 1, pos=pos)
        self.playersPrePos[name] = np.array(self.players[name].robot.pos)
        self.players[name].initObservation(self.grid.currentMap.shape)

    def removePlayer(self, name):
        del self.players[name]

    def getCanvas(self):
        canvas = self.grid.getCanvas()
        pt = QPainter(canvas)
        pt.setBrush(QColor("#aa66ccff"))
        r = 5
        for p in self.players.values():
            pos = p.robot.pos
            pt.drawEllipse(pos[0]-r, pos[1]-r, 2*r, 2*r)
        return canvas

