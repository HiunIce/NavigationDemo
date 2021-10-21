import cv2
import numpy as np
import utils


class RRTArgs:
    def __init__(self):
        self.move_dis = 10
        self.direct_rate = 0.3

        self.brave_rate = 0.6
        self.br_changeRate = 0.96
        self.brave_scale = 5
        self.bs_changeRate = 0.6
        self.end_check_dis = 6
        self.maxSampleTimes = 1999


class RRT:
    def __init__(self, cmap, pos, tar, ok=0, args=None):

        self.__posList = []
        self.__parentList = []
        self.cmap = cmap
        self.pos = pos
        self.target = tar
        self.ok_val = ok

        self.__posList.append(pos)
        self.__parentList.append(-1)
        ##############
        if args:
            self.args = args
        else:
            self.args = RRTArgs()
        self.modify_line = True
        self.sampleTimes = 0
        #######
        self.show_map = None
        self.displayCallBack = None

    @staticmethod
    def fast_search(cmap, pos, tar, ok=0, displayCallback=None, args=None):
        if (pos[0] == tar[0]) and (pos[1] == tar[1]):
            return np.array([])
        if args is not None:
            rrt = RRT(cmap, pos, tar, ok, args=args)
        else:
            rrt = RRT(cmap, pos, tar, ok)
        rrt.displayCallBack = displayCallback
        if displayCallback is not None:
            rrt.show_map = cmap.copy()
        return rrt.run()

    def samplePnt(self):
        self.sampleTimes += 1
        if np.random.rand() < self.args.direct_rate:
            return self.target
        x = np.random.randint(0, self.cmap.shape[0])
        y = np.random.randint(0, self.cmap.shape[1])
        return x, y

    def run(self):
        if self.displayCallBack is not None:
            cv2.circle(self.show_map, self.pos, 10, 255, 1)
            cv2.circle(self.show_map, self.target, 10, 255, 1)
            self.tempmap = self.show_map.copy()
        while not self.addNextNode():
            pass
        return self.getTrajectory()

    def addNextNode(self):
        res = False
        if self.displayCallBack is not None:
            self.show_map = self.tempmap.copy()
        # find a random point
        br = self.args.brave_rate
        bs = self.args.brave_scale
        bad_times = 0
        while not res:
            if self.sampleTimes > self.args.maxSampleTimes:
                print('give up')
                return True
            tar = self.samplePnt()
            #print('random sample', tar)
            idx = self.findClosestNodeIdx(tar)
            p = self.__posList[idx]
            dir = np.array(tar) - np.array(p)
            dis = np.linalg.norm(dir)
            dir = dir/(dis+0.001)
            md = self.args.move_dis if np.random.rand() < br else self.args.move_dis * bs
            tar = (p + dir * md).astype(np.int32)
            #print(p, 'and the filtered pnt is', tar)
            da = np.linalg.norm(np.array(self.target) - np.array(p))
            #print('the dis is', de)
            if da < self.args.end_check_dis:  # check if finished
                res, pos = collision_judge_rrt(self.cmap, self.target, p, ok=self.ok_val)
                if res:
                    self.__parentList.append(idx)
                    self.__posList.append(self.target)
                    return True
            res, pos = collision_judge_rrt(self.cmap, p, tar)
            # Change Args
            bad_times += 1
            br = br * self.args.br_changeRate
            bs = bs * self.args.bs_changeRate

            if self.displayCallBack is not None:
                cv2.circle(self.show_map, tar, 2, 255, 1)
                self.displayCallBack(self.show_map)
        if self.displayCallBack is not None:
            cv2.circle(self.tempmap, p, 3, 64, -1)
        #print(idx, p)
        self.__posList.append(tar)
        self.__parentList.append(idx)
        if self.displayCallBack is not None:
            cv2.line(self.tempmap, tar, p, 128, 1, 4, 0)
        return False

    @staticmethod
    def distance(p1, p2):
        return np.linalg.norm(np.array(p1)-np.array(p2))

    def findClosestNodeIdx(self, pnt):
        dis = [RRT.distance(pnt, p) for p in self.__posList]
        m = min(dis)
        idx = dis.index(m)
        return idx

    def getTrajectory(self):
        idx = self.__parentList[-1]
        poslist = [self.__posList[-1]]
        while (idx != -1):
            poslist.append(self.__posList[idx])
            idx = self.__parentList[idx]
        poslist.reverse()
        if self.modify_line:
            poslist = self.modifyLine(poslist)
        #self.finalCheck(self.cmap, poslist)
        #print('after modified', poslist)
        return poslist

    def modifyLine(self, pnts):
        num = len(pnts)
        start = 0
        npts = []
        while start < num-1:
            npts.append(pnts[start])
            #print('append', start)
            for i in range(num-1, start, -1):
                res, pos = collision_judge_rrt(self.cmap, pnts[start], pnts[i])
                #print(res, pos, start, i, num, '??', pnts[start], pnts[i])
                if res:
                    start = i-1
                    break
            start = start + 1
        npts.append(pnts[-1])
        return npts

    @staticmethod
    def finalCheck(cmap, pnts):
        #print('final check~~~~~~~~~')
        for i in range(len(pnts)-1):
            p1 = pnts[i]
            p2 = pnts[i+1]
            res, pos = utils.collision_judge(cmap, p1, p2)
            #print(res, pos, '????', p1, p2)


from skimage.draw import draw

def collision_judge_rrt(map, pos, ep, ok=0):
    rr, cc = draw.line(pos[1], pos[0], ep[1], ep[0])
    ep = pos
    for r, c in zip(rr, cc):
        if (r == pos[1]) and (c == pos[0]):
            continue
        rf = (r >= 0) and (c >=0) and (r < map.shape[0]) and (c < map.shape[1])
        if rf and (map[r, c] == ok):
            ep = [c, r]
        else:
            return False, ep
    return True, ep


if __name__ == "__main__":
    import RRT_Test
    RRT_Test.testWithAnimation()