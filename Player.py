import numpy as np

from MobileRobot import MobileRobot
import queue
import rrtUtils

from RRTBase import RRT, RRTArgs

import matplotlib.pyplot as plt

import cv2

class Player:
    def __init__(self, name, idx, pos):
        self.name = name
        self.viewMap = None
        self.decisionList = queue.Queue()
        self.idx = idx
        self.robot = MobileRobot(self.idx, pos=pos)
        self.viewRadius = 20
        self.fronts = []
        self.target = None
        self.explore_rate = 0.0

        self.rrt_args_fast = RRTArgs()
        self.rrt_args_fast.maxSampleTimes = 50
        self.rrt_args_fast.direct_rate = 0.7

        self.rrt_args_normal = RRTArgs()
        self.rrt_args_normal.maxSampleTimes = 500
        self.pre_idx = -1

    def initObservation(self, shape):
        self.viewMap = np.zeros(shape=shape, dtype=np.uint16)
        self.wallMap = np.zeros(shape=shape, dtype=np.uint8)

    def clearDecision(self):
        self.decisionList = queue.Queue()

    def closest(self):
        # Todo: you need to find an index, to make program work

        if idx == self.pre_idx:
            # print('avoid holds a bug')
            idx = np.random.randint(0, diff.shape[0], 1)[0]
        tar = self.fronts[idx]
        self.pre_idx = idx
        return tar

    def planTheory(self):
        if not self.decisionList.empty():
            return
        self.target = self.closest()
        self.moveTheory(self.target)

    def moveTheory(self, tar):
        # Todo: you can change self.rrt_args_fast to accelarte your program.
        dis = self.robot.pos - tar
        if np.linalg.norm(dis) < 20:
            res, pos = rrtUtils.collision_judge(self.wallMap, self.robot.pos, tar)
            if res:
                traj = rrtUtils.moveDirectly(self.robot.pos, tar)
            else:
                traj = RRT.fast_search(self.wallMap, self.robot.pos, tar, ok=0, args=self.rrt_args_fast)
        else:
            traj = RRT.fast_search(self.wallMap, self.robot.pos, tar, ok=0, args=self.rrt_args_normal)
        acts = rrtUtils.traj2acts(traj)
        self.putActions(acts)

    def moveTheory_cheat(self, cmap, tar):
        traj = RRT.fast_search(cmap, self.robot.pos, tar)
        acts = rrtUtils.traj2acts(traj)
        self.putActions(acts)

    def putActions(self, acts):
        pre = self.decisionList.qsize()
        for a in acts:
            if (a[0] == 0) and (a[1] == 0):
                continue
            self.decisionList.put(a)

    def act(self, cmap):
        if self.decisionList.qsize() == 0:
            print('no actions left')
            return
        action = self.decisionList.get()
        res, pos = rrtUtils.collision_judge(cmap, self.robot.pos, self.robot.pos + action)
        #res, pos = utils.collision_judge(cmap, self.robot.pos, action)
        #res, pos = utils.collision_judge_step_fast(cmap, self.robot.pos, action)
        if not res:
            # directly give up all
            self.clearDecision()
            print(self.robot.pos+action, 'ready to give up all',
                  self.robot.pos, action, '---->', pos, 'real, left:', self.decisionList.qsize())
        self.robot.pos = pos # [100,100]

        y0, y1, x0, x1 = rrtUtils.getRangeMap(self.robot.pos, self.viewRadius, cmap.shape)

        obs = cmap[y0:y1, x0:x1]
        pos_t = [self.robot.pos[0] - x0, self.robot.pos[1] - y0]
        mp, wall = rrtUtils.getSampleLine(obs, pos_t, self.viewRadius)

        self.viewMap[y0:y1, x0:x1] += mp
        self.viewMap[pos[1], pos[0]] = 255
        self.viewMap[self.viewMap > 255] = 255

        self.fronts = rrtUtils.getFrontier(self.viewMap.astype(np.uint8), self.wallMap)
        if wall.shape[0] != 0:
            for w in wall:
                self.wallMap[w[0]+y0, w[1]+x0] = 255


    def getExploreRate(self):
        self.explore_rate = np.sum(self.viewMap/255) / (self.viewMap.shape[0]*self.viewMap.shape[1])
        return self.explore_rate
        
    def getPlayerView(self):
        return rrtUtils.drawUserView(self.viewMap.astype(np.uint8), self.wallMap,
                                     self.fronts, [self.robot.pos, self.target])

