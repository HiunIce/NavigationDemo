import cv2
import numpy as np
from skimage import draw
import utils


import matplotlib.pyplot as plt

class RRT:
    def __init__(self, cmap, pos, tar, ok=0):

        self.__posList = []
        self.__parentList = []
        self.cmap = cmap
        self.pos = pos
        self.target = tar
        self.ok_val = ok

        self.__posList.append(pos)
        self.__parentList.append(-1)
        ##############
        self.move_dis = 10
        self.direct_rate = 0.2
        self.brave_rate = 0.3
        self.brave_scale = 5
        self.end_check_dis = 6
        self.modify_line = True
        #######
        self.show_map = None
        self.displayCallBack = None

    @staticmethod
    def fast_search(cmap, pos, tar, ok=255, displayCallback=None):
        rrt = RRT(cmap, pos, tar, ok)
        rrt.displayCallBack = displayCallback
        if displayCallback is not None:
            rrt.show_map = cmap.copy()
        return rrt.run()

    def samplePnt(self):
        if np.random.rand() < self.direct_rate:
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
        br = self.brave_rate
        bs = self.brave_scale
        bad_times = 0
        while not res:
            tar = self.samplePnt()
            #print('random sample', tar)
            idx = self.findClosestNodeIdx(tar)
            p = self.__posList[idx]
            dir = np.array(tar) - np.array(p)
            dis = np.linalg.norm(dir)
            #print(self.target, tar)
            dir = dir/(dis+0.001)
            md = self.move_dis if np.random.rand() < br else self.move_dis * bs
            tar = (p + dir * md).astype(np.int32)
            #print(p, 'and the filtered pnt is', tar)
            da = np.linalg.norm(np.array(self.target) - np.array(p))
            de = np.linalg.norm(np.array(self.target) - np.array(tar))
            #print('the dis is', de)
            if da< self.end_check_dis: # check if finished
                res, pos = utils.collision_judge(self.cmap, self.target, p)
                if res:
                    #print('ready to get rid', self.target, tar)
                    self.__parentList.append(idx)
                    #self.__parentList.append(len(self.__parentList))
                    self.__posList.append(self.target)
                    #self.__posList.append(self.target)
                    return True
            res, pos = utils.collision_judge(self.cmap, p, tar)
            bad_times += 1
            br = br * 0.99
            bs = bs * 0.6
            #print(res, pos)
            if self.displayCallBack is not None:
                cv2.circle(self.show_map, tar, 2, 255, 1)
                self.displayCallBack(self.show_map)
            # plt.imshow(self.show_map, 'gray')
            # #plt.show()
            # plt.pause(0.1)
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
                res, pos = utils.collision_judge(self.cmap, pnts[start], pnts[i])
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


def test_RRT(displayCallback=None):
    import cv2
    def makeTestGrid(shape=(300, 300)):
        bm = np.zeros(shape=shape, dtype=np.uint8)
        seeds = [1,2,3,4,5,6,7,8,9,10]
        np.random.seed(18)
        for i in range(10):
            #np.random.seed(seeds[i])
            p1 = np.random.randint(0, bm.shape[0], 2)
            p2 = np.copy(p1)
            p2[np.random.randint(0, 2)] = np.random.randint(0, 100)
            cv2.line(bm, p1, p2, 255, thickness=3, lineType=4, shift=0)
        return bm
    bm = makeTestGrid()

    pos = [100, 100]
    tar = [250, 250]
    rs = RRT.fast_search(bm, pos, tar, displayCallback=displayCallback)

    cv2.circle(bm, pos, 10, 255, 1)
    cv2.circle(bm, tar, 10, 255, 1)

    for p in rs:
        cv2.circle(bm, p, 3, 255, -1)

    for idx in range(len(rs) - 1):
        cv2.line(bm, rs[idx], rs[idx + 1], 255, 1, 4, 0)

    if not displayCallback:
        plt.imshow(bm)
        plt.show()
    else:
        pass
        displayCallback(bm, add=rs)



def testWithAnimation():
    from PyQt5.QtGui import QPainter, QImage, QColor
    from PyQt5.QtWidgets import QWidget, QApplication
    import sys
    import utils
    class showWidget(QWidget):
        def __init__(self, parent=None):
            QWidget.__init__(self, parent=parent)
            self.img = None

        def paintEvent(self, a0):
            pt = QPainter(win)
            if self.img is not None:
                pt.drawImage(self.rect(), utils.toQImage(self.img))

        def setInputImg(self, img):
            self.img = img
            self.update()

        def drawFinishLine(self, rs):
            self.img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
            for idx in range(len(rs) - 1):
                p0 = rs[idx]
                p1 = rs[idx + 1]
                #print(p0, '--->', p1)
                cv2.line(self.img, rs[idx], rs[idx + 1], (255,0,0), 1, 4, 0)
            print('draw line fin')
            self.update()

        def start(self):
            def callback(a, **kargs):
                if 'add' in kargs.keys():
                    win.drawFinishLine(kargs['add'])
                else:
                    win.setInputImg(a)
                QApplication.processEvents()
            test_RRT(callback)


    app = QApplication(sys.argv)
    win = showWidget()
    win.show()
    win.start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    testWithAnimation()