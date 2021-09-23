import numpy as np

from MobileRobot import MobileRobot
import queue
import utils


class Player:
    def __init__(self, name, idx):
        self.name = name
        self.viewMap = None
        self.decisionList = queue.Queue()
        self.idx = idx
        self.robot = MobileRobot(self.idx, pos=[100, 100])
        self.viewRadius = 20

    def initObservation(self, shape):
        self.viewMap = np.zeros(shape=shape, dtype=np.uint8)

    def act(self, cmap):
        if self.decisionList.qsize() == 0:
            return

        action = self.decisionList.get()
        res, pos = utils.collision_judge(cmap, self.robot.pos, action)
        self.robot.pos = pos  # [100,100]

        y0, y1, x0, x1 = utils.getRangeMap(self.robot.pos, self.viewRadius, cmap.shape)
        print(x0, x1, y0, y1, self.robot.pos)

        obs = cmap[y0:y1, x0:x1]
        pos_t = [self.robot.pos[0] - x0, self.robot.pos[1] - y0]
        self.viewMap[y0:y1, x0:x1] += utils.getSampleLine(obs, pos_t, self.viewRadius)
        self.viewMap[self.viewMap > 255] = 255
