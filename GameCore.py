
from GameGrid import GameGrid
from Player import Player
from PyQt5.QtGui import QPainter, QColor
import utils

class GameCore:
    def __init__(self, shape=(1000, 1000)):
        self.grid = GameGrid(shape)
        self.players = dict()
        self.addPlayer('host')

    def nextFrame(self):
        self.grid.updateGameGrid(self.players.values())
        for v in self.players.values():
            v.act(self.grid.currentMap)


    def setHostInput(self, action):
        self.players['host'].decisionList.put(action)

    def getHostView(self):
        return utils.toQImage(self.players['host'].viewMap)

    def addPlayer(self, name):
        self.players[name] = Player(name, len(self.players) + 1)
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

