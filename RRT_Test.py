
import numpy as np
import cv2
from numpy.core.fromnumeric import shape
from RRTBase import RRT, RRTArgs
import matplotlib.pyplot as plt

test_rrt_seed = -1

def test_RRT(displayCallback=None, grid=None, args=None):
    import cv2
    def makeTestGrid(shape=(300, 300)):
        bm = np.zeros(shape=shape, dtype=np.uint8)
        if test_rrt_seed >= 0:
            np.random.seed(test_rrt_seed)
        for i in range(10):
            p1 = np.random.randint(0, bm.shape[0], 2)
            p2 = np.copy(p1)
            p2[np.random.randint(0, 2)] = np.random.randint(0, 100)
            cv2.line(bm, p1, p2, 255, thickness=3, lineType=4, shift=0)
        return bm
    if grid is not None:
        bm = grid[0]
        print(bm)
        print(grid[1], grid[2])
        pos = np.array(grid[1]).astype(np.int64)
        tar = np.array(grid[2]).astype(np.int64)
    else:
        bm = makeTestGrid()
        pos = [100, 100]
        tar = [250, 250]

    rs = RRT.fast_search(bm, pos, tar, displayCallback=displayCallback, args=args)

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


def testWithAnimation(t_map=None, args=None):
    from PyQt5.QtGui import QPainter, QImage, QColor
    from PyQt5.QtWidgets import QWidget, QApplication
    import sys
    import rrtUtils
    class showWidget(QWidget):
        def __init__(self, parent=None):
            QWidget.__init__(self, parent=parent)
            self.img = None

        def paintEvent(self, a0):
            pt = QPainter(win)
            if self.img is not None:
                pt.drawImage(self.rect(), rrtUtils.toQImage(self.img))

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

        def start(self, grid=None):
            def callback(a, **kargs):
                if 'add' in kargs.keys():
                    win.drawFinishLine(kargs['add'])
                else:
                    win.setInputImg(a)
                QApplication.processEvents()
            test_RRT(callback, grid, args=args)


    app = QApplication(sys.argv)
    win = showWidget()
    win.show()
    win.start(t_map)

    sys.exit(app.exec_())



# TODO Run all the cases, and know how to use arguments of RRT
""" Args:
        self.move_dis = 10
        self.direct_rate = 0.3
        self.brave_rate = 0.6
        self.br_changeRate = 0.96
        self.brave_scale = 5
        self.bs_changeRate = 0.6
        self.end_check_dis = 6
        self.maxSampleTimes = 1999
"""

def case_0():
    # when everything is ok
    m = np.zeros(shape=(300, 300), dtype=np.uint8)
    m[30: 280, 30: 280] = 255
    start, end = [0, 0], [299, 299]
    arg = RRTArgs()

    testWithAnimation([m, start, end], arg)

def case_1():
    # when can not finish
    m = np.zeros(shape=(300, 300), dtype=np.uint8)
    m[0:, 100] = 255
    start, end = [0, 0], [250, 250]
    arg = RRTArgs()
    
    # TODO: in this case, change which arguments will finish earlyer?
    # arg.move_dis = 30 # change arguments like that

    testWithAnimation([m, start, end], arg)

def case_2():
        # when can not finish
    m = np.zeros(shape=(300, 300), dtype=np.uint8)
    m[0: 300, 97] = 255
    m[0: 290, 103] = 255
    m[289, 103:] = 255
    m[299, 97:] = 255
    start, end = [100, 0], [299, 297]
    arg = RRTArgs()
    
    # TODO: in this case, you can not let the rrt give up
    # And change which args will make RRT faster?
    # Explain why.
    
    testWithAnimation([m, start, end], arg)

def case_3():
        # when can not finish
    m = np.zeros(shape=(300, 300), dtype=np.uint8)
    m[0: 290, 103] = 255
    m[289, 103:285] = 255
    m[299, 97:285] = 255
    start, end = [100, 0], [299, 10]
    arg = RRTArgs()
    
    # TODO: in this case, finish searching in 5000 steps
    # Explain why.
    arg.maxSampleTimes = 3000

    testWithAnimation([m, start, end], arg)


if __name__ == "__main__":
    # case_0() # only for check
    # case_1() # TODO 1
    # case_2() # TODO 2
    case_3() # TODO 3