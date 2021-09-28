import numpy as np

from MobileRobot import MobileRobot
import queue
import utils

from RRTBase import RRT

class Player:
    def __init__(self, name, idx):
        self.name = name
        self.viewMap = None
        self.decisionList = queue.Queue()
        self.idx = idx
        self.robot = MobileRobot(self.idx, pos=[100, 100])
        self.viewRadius = 20
        self.fronts = []

    def initObservation(self, shape):
        self.viewMap = np.zeros(shape=shape, dtype=np.uint16)
        self.wallMap = np.zeros(shape=shape, dtype=np.uint8)

    def clearDecision(self):
        self.decisionList = queue.Queue()

    def planTheory(self, cmap):
        self.moveTheory(cmap, self.fronts[-1])

    def moveTheory(self, cmap, tar):
        traj = RRT.fast_search(cmap, self.robot.pos, tar)
        acts = utils.traj2acts(traj)
        for a in acts:
            self.decisionList.put(a)

    def act(self, cmap):
        if self.decisionList.qsize() == 0:
            return

        action = self.decisionList.get()
        res, pos = utils.collision_judge(cmap, self.robot.pos, self.robot.pos + action)
        #res, pos = utils.collision_judge(cmap, self.robot.pos, action)
        self.robot.pos = pos  # [100,100]

        y0, y1, x0, x1 = utils.getRangeMap(self.robot.pos, self.viewRadius, cmap.shape)

        obs = cmap[y0:y1, x0:x1]
        pos_t = [self.robot.pos[0] - x0, self.robot.pos[1] - y0]
        mp, wall = utils.getSampleLine(obs, pos_t, self.viewRadius)
 
        self.viewMap[y0:y1, x0:x1] += mp
        self.viewMap[self.viewMap > 255] = 255

        self.fronts = utils.getFrontier(self.viewMap.astype(np.uint8), self.wallMap)
        
        if wall.shape[0] != 0:
            for w in wall:
                self.wallMap[w[0]+y0,w[1]+x0] = 255

    def getExploreRate(self):
        return np.sum(self.viewMap/255) / (self.viewMap.shape[0]*self.viewMap.shape[1])
        
    def getPlayerView(self):
        return utils.drawUserView(self.viewMap.astype(np.uint8), self.wallMap, self.fronts)

